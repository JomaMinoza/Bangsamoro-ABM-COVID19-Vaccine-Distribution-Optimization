from mesa.visualization.modules import BarChartModule

class DistributionChartModule(BarChartModule):
    default_fields = [
                {"Label": "0 - 9", "Color": "#7EF9FF"},
                {"Label": "10 - 19", "Color": "#B0DFE5"},
                {"Label": "20 - 29", "Color": "#73C2FB"},
                {"Label": "30 - 39", "Color": "#57A0D3"},
                {"Label": "40 - 49", "Color": "#0080FF"},
                {"Label": "50 - 59", "Color": "#0F52BA"},
                {"Label": "60 - 69", "Color": "#1034A6"},
                {"Label": "70 - 79", "Color": "#003152"},
                {"Label": "80 and above", "Color": "#111E6C"}
    ]
    
    def __init__(self, 
                 canvas_width, 
                 canvas_height, 
                 data_collector = "datacollector", 
                 fields = default_fields, 
                 geospatial = False, 
                 location_index = 0
                ):
        super().__init__(
            fields              = fields,
            canvas_width        = canvas_width,
            canvas_height       = canvas_height,
            data_collector_name = data_collector,
            geospatial          = geospatial,
            location_index      = location_index
        )