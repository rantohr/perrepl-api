from dataclasses import dataclass, field, asdict
from typing import List, Dict

@dataclass(frozen=True)
class CotationDataset:
    hotels: str = field(default='Hotel', metadata={"description": "application name as field and Model name as value"})
    activities: str = field(default='Activity', metadata={"description": "application name as field and Model name as value"})
    transports: str = field(default='Transport', metadata={"description": "application name as field and"})

    def to_dict(self):
        return asdict(self)
    
