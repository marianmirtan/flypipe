var tags = ["t4", "t2", "t9", "scale", "t6", "model", "t7", "split", "t0", "train", "raw.table", "t1", "t10", "t3", "t8", "t5", "datasource"];
var nodes = [{"name": "raw.table", "position": [1.0, 50.0], "active": true, "run_status": {"bg-class": "info", "bg-color": "#0dcaf0", "text": "ACTIVE"}, "type": {"shape": "circle", "bg-class": "danger", "bg-color": "#dc3545", "text": "PySpark"}, "node_type": "DATASOURCE", "dependencies": [], "successors": ["t0"], "definition": {"description": "Spark table raw.table", "tags": ["datasource"], "columns": []}}, {"name": "t0", "position": [2.0, 50.0], "active": true, "run_status": {"bg-class": "info", "bg-color": "#0dcaf0", "text": "ACTIVE"}, "type": {"shape": "circle", "bg-class": "danger", "bg-color": "#dc3545", "text": "PySpark"}, "node_type": "TRANSFORMATION", "dependencies": ["raw.table"], "successors": ["t5", "t6"], "definition": {"description": "No description", "tags": [], "columns": [{"name": "dummy", "type": "Decimal", "description": "No description"}]}}, {"name": "t5", "position": [3.0, 50.0], "active": false, "run_status": {"bg-class": "dark", "bg-color": "#212529", "text": "SKIPPED"}, "type": {"shape": "circle", "bg-class": "success", "bg-color": "#198754", "text": "Pandas"}, "node_type": "TRANSFORMATION", "dependencies": ["t0"], "successors": ["t4", "t2"], "definition": {"description": "No description", "tags": [], "columns": [{"name": "dummy", "type": "Integer", "description": "No description"}]}}, {"name": "t4", "position": [4.0, 33.33], "active": false, "run_status": {"bg-class": "dark", "bg-color": "#212529", "text": "SKIPPED"}, "type": {"shape": "circle", "bg-class": "warning", "bg-color": "#ffc107", "text": "Pandas on Spark"}, "node_type": "TRANSFORMATION", "dependencies": ["t5"], "successors": ["t2"], "definition": {"description": "No description", "tags": [], "columns": [{"name": "dummy", "type": "Integer", "description": "No description"}]}}, {"name": "t6", "position": [4.0, 66.67], "active": true, "run_status": {"bg-class": "info", "bg-color": "#0dcaf0", "text": "ACTIVE"}, "type": {"shape": "circle", "bg-class": "success", "bg-color": "#198754", "text": "Pandas"}, "node_type": "TRANSFORMATION", "dependencies": ["t0"], "successors": ["t3", "t7", "t8"], "definition": {"description": "No description", "tags": [], "columns": [{"name": "dummy", "type": "Integer", "description": "No description"}]}}, {"name": "t2", "position": [5.0, 25.0], "active": false, "run_status": {"bg-class": "dark", "bg-color": "#212529", "text": "SKIPPED"}, "type": {"shape": "circle", "bg-class": "success", "bg-color": "#198754", "text": "Pandas"}, "node_type": "TRANSFORMATION", "dependencies": ["t4", "t5"], "successors": ["t1", "t9"], "definition": {"description": "No description", "tags": [], "columns": [{"name": "dummy", "type": "Integer", "description": "No description"}]}}, {"name": "t3", "position": [5.0, 50.0], "active": true, "run_status": {"bg-class": "info", "bg-color": "#0dcaf0", "text": "ACTIVE"}, "type": {"shape": "circle", "bg-class": "danger", "bg-color": "#dc3545", "text": "PySpark"}, "node_type": "TRANSFORMATION", "dependencies": ["t6"], "successors": ["t1"], "definition": {"description": "No description", "tags": [], "columns": [{"name": "dummy", "type": "Integer", "description": "No description"}]}}, {"name": "t7", "position": [5.0, 75.0], "active": true, "run_status": {"bg-class": "info", "bg-color": "#0dcaf0", "text": "ACTIVE"}, "type": {"shape": "circle", "bg-class": "success", "bg-color": "#198754", "text": "Pandas"}, "node_type": "TRANSFORMATION", "dependencies": ["t6"], "successors": ["t1"], "definition": {"description": "No description", "tags": [], "columns": [{"name": "dummy", "type": "Integer", "description": "No description"}]}}, {"name": "t1", "position": [6.0, 50.0], "active": true, "run_status": {"bg-class": "info", "bg-color": "#0dcaf0", "text": "ACTIVE"}, "type": {"shape": "circle", "bg-class": "success", "bg-color": "#198754", "text": "Pandas"}, "node_type": "TRANSFORMATION", "dependencies": ["t2", "t3", "t7"], "successors": ["t8"], "definition": {"description": "No description", "tags": [], "columns": [{"name": "dummy", "type": "Integer", "description": "No description"}]}}, {"name": "t8", "position": [7.0, 33.33], "active": true, "run_status": {"bg-class": "info", "bg-color": "#0dcaf0", "text": "ACTIVE"}, "type": {"shape": "circle", "bg-class": "danger", "bg-color": "#dc3545", "text": "PySpark"}, "node_type": "TRANSFORMATION", "dependencies": ["t1", "t6"], "successors": ["t10"], "definition": {"description": "No description", "tags": ["model", "split"], "columns": [{"name": "dummy", "type": "Integer", "description": "No description"}]}}, {"name": "t9", "position": [7.0, 66.67], "active": true, "run_status": {"bg-class": "info", "bg-color": "#0dcaf0", "text": "ACTIVE"}, "type": {"shape": "circle", "bg-class": "danger", "bg-color": "#dc3545", "text": "PySpark"}, "node_type": "TRANSFORMATION", "dependencies": ["t2"], "successors": ["t10"], "definition": {"description": "No description", "tags": ["model", "scale"], "columns": [{"name": "dummy", "type": "Integer", "description": "No description"}]}}, {"name": "t10", "position": [8.0, 50.0], "active": true, "run_status": {"bg-class": "info", "bg-color": "#0dcaf0", "text": "ACTIVE"}, "type": {"shape": "circle", "bg-class": "danger", "bg-color": "#dc3545", "text": "PySpark"}, "node_type": "TRANSFORMATION", "dependencies": ["t8", "t9"], "successors": [], "definition": {"description": "No description", "tags": ["model", "train"], "columns": [{"name": "dummy", "type": "Integer", "description": "No description"}]}}];
var links = [{"source": "t8", "source_position": [7.0, 33.33], "target": "t10", "target_position": [8.0, 50.0], "active": true}, {"source": "t1", "source_position": [6.0, 50.0], "target": "t8", "target_position": [7.0, 33.33], "active": true}, {"source": "t2", "source_position": [5.0, 25.0], "target": "t1", "target_position": [6.0, 50.0], "active": true}, {"source": "t2", "source_position": [5.0, 25.0], "target": "t9", "target_position": [7.0, 66.67], "active": true}, {"source": "t4", "source_position": [4.0, 33.33], "target": "t2", "target_position": [5.0, 25.0], "active": false}, {"source": "t5", "source_position": [3.0, 50.0], "target": "t4", "target_position": [4.0, 33.33], "active": false}, {"source": "t5", "source_position": [3.0, 50.0], "target": "t2", "target_position": [5.0, 25.0], "active": false}, {"source": "t0", "source_position": [2.0, 50.0], "target": "t5", "target_position": [3.0, 50.0], "active": false}, {"source": "t0", "source_position": [2.0, 50.0], "target": "t6", "target_position": [4.0, 66.67], "active": true}, {"source": "raw.table", "source_position": [1.0, 50.0], "target": "t0", "target_position": [2.0, 50.0], "active": true}, {"source": "t3", "source_position": [5.0, 50.0], "target": "t1", "target_position": [6.0, 50.0], "active": true}, {"source": "t6", "source_position": [4.0, 66.67], "target": "t3", "target_position": [5.0, 50.0], "active": true}, {"source": "t6", "source_position": [4.0, 66.67], "target": "t7", "target_position": [5.0, 75.0], "active": true}, {"source": "t6", "source_position": [4.0, 66.67], "target": "t8", "target_position": [7.0, 33.33], "active": true}, {"source": "t7", "source_position": [5.0, 75.0], "target": "t1", "target_position": [6.0, 50.0], "active": true}, {"source": "t9", "source_position": [7.0, 66.67], "target": "t10", "target_position": [8.0, 50.0], "active": true}];