from .battery_base import BatteryBase
import numpy as np

class Battery_NMC(BatteryBase):
    """repräsentiert das gesamte Pack aus n_series×n_parallel Zellen"""
    
    cell_r_mOhm = 7.0
    # OCV-Kennlinie
    cell_soc_table = np.array([
        0.00, 0.04, 0.09, 0.13, 0.17, 0.21,
        0.26, 0.30, 0.40, 0.52, 0.64, 0.76,
        0.88, 1.00
    ])
    # Werte sind geteilt durch 10 -> Wert pro Zelle
    cell_ocv_table = np.array([
        3.20, 3.261, 3.317, 3.385, 3.424, 3.466,
        3.539, 3.565, 3.665, 3.764, 3.891, 4.014,
        4.108, 4.20
    ])

    def __init__(self, capacity_nom_Ah_cell, n_series=10, n_parallel=1, initial_soc=1.0):
        pack_capacity_Ah = capacity_nom_Ah_cell * n_parallel
        pack_resistance_mOhm = self.cell_r_mOhm * n_series / n_parallel
        super().__init__(
            capacity_nom_Ah=pack_capacity_Ah,
            internal_resistance_mOhm=pack_resistance_mOhm,
            initial_soc=initial_soc,
        )

        self.soc_table = self.cell_soc_table
        self.ocv_table = self.cell_ocv_table * n_series
