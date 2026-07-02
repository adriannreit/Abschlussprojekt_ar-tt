import numpy as np

class BatteryBase:
    def __init__(
        self,
        capacity_nom_Ah,
        internal_resistance_mOhm,
        initial_soc=1.0
    ):
        self.C_nom = capacity_nom_Ah * 3600
        self.soc = initial_soc
        self.R_int = internal_resistance_mOhm * 1e-3

    def is_empty(self) -> bool:
        return self.soc <= 0.0 + 1e-9

    def is_full(self) -> bool:
        return self.soc >= 1.0 - 1e-9
    
    def apply_current(self, current: float, duration: float) -> None:
        dsoc = -(current * duration) / self.C_nom
        self.soc = max(0.0, min(self.soc + dsoc, 1.0))

    def voltage(self, current: float = 0.0) -> float:
        open_circuit_voltage = np.interp(self.soc, self.soc_table, self.ocv_table)
        return open_circuit_voltage - self.R_int * current

    def __str__(self):
        return f"Battery(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"
