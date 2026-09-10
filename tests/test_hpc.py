"""Tests RATISS-HPC — cluster, thermique, énergie, performances."""

import numpy as np

from ratiss_hpc.cluster import (Cluster, SBCNode, benchmark_relative,
                                solar_autonomy_hours, thermal_safe)


class TestCluster:
    def test_standard_has_8_nodes(self):
        assert len(Cluster.standard(8).nodes) == 8

    def test_total_cores(self):
        assert Cluster.standard(8).total_cores() == 64

    def test_power_scales_with_load(self):
        c = Cluster.standard(8)
        assert c.power_w(1.0) > c.power_w(0.0)

    def test_power_scales_with_nodes(self):
        assert Cluster.standard(16).power_w(1.0) > Cluster.standard(8).power_w(1.0)


class TestThermal:
    def test_active_cooling_cooler_than_passive(self):
        c = Cluster.standard(8)
        t_active = thermal_safe(c, 1.0, active_cooling=True)["cpu_temp_c"]
        t_passive = thermal_safe(c, 1.0, active_cooling=False)["cpu_temp_c"]
        assert t_active < t_passive

    def test_full_load_safe_with_active_cooling(self):
        c = Cluster.standard(8)
        assert thermal_safe(c, 1.0, active_cooling=True)["safe"]

    def test_temp_rises_with_load(self):
        c = Cluster.standard(8)
        assert c.cpu_temp_c(1.0) > c.cpu_temp_c(0.0)


class TestEnergy:
    def test_autonomy_positive(self):
        assert solar_autonomy_hours(Cluster.standard(8), 14.3) > 0

    def test_bigger_battery_more_autonomy(self):
        c = Cluster.standard(8)
        assert solar_autonomy_hours(c, 28.7) > solar_autonomy_hours(c, 14.3)

    def test_daily_energy_reasonable(self):
        c = Cluster.standard(8)
        e = c.daily_energy_wh(np.full(24, 0.7))
        assert 500 < e < 3000  # ~1-2 kWh/jour pour 8 SBC


class TestBenchmark:
    def test_speedup_sublinear(self):
        # loi d'Amdahl : speedup < nb noeuds
        r = benchmark_relative(Cluster.standard(8))
        assert r["speedup_vs_single"] < 8.0
        assert r["efficiency"] < 1.0

    def test_more_nodes_faster(self):
        assert (benchmark_relative(Cluster.standard(16))["speedup_vs_single"]
                > benchmark_relative(Cluster.standard(8))["speedup_vs_single"])

    def test_speedup_saturates(self):
        # overhead linéaire : le speedup plafonne à 1/s = 10×
        assert benchmark_relative(Cluster.standard(64))["speedup_vs_single"] < 10.0


class TestFigureGeneration:
    def test_all_figures_valid(self, tmp_path):
        import scripts.generate_figures as g
        g.OUT = str(tmp_path)
        g.fig_plan_architecture(); g.fig_plan_thermique(); g.fig_appareil_monte()
        g.fig_performances(); g.fig_energie_journaliere(); g.fig_carte_thermique()
        g.fig_logo()
        for n in ["01_plan_architecture.png", "02_plan_thermique.png",
                  "03_appareil_monte.png", "04_performances.png",
                  "06_energie_journaliere.png", "07_carte_thermique.png",
                  "05_logo_ratis_labs.png"]:
            p = tmp_path / n
            assert p.exists() and p.stat().st_size > 1000


class TestPhysicsValidation:
    def test_validate_physics_all_pass(self):
        import scripts.validate_physics as v
        assert v.main() == 0
