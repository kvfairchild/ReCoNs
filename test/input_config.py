node_data = [
	["root_node", "concept"], 
	["register1", "register"], 
	["register2", "register"], 
	["register3", "register"], 
	["register4", "register"], 
	["register5", "register"], 
	["register6", "register"], 
	["register7", "register"],	
	["register8", "register"],	
	["register9", "register"],	
	["exit_node", "concept"]
]

link_data = [
	{
		"origin": ["root_node", "gen"],
		"target": ["register1", "gen"]
	},
	{
		"origin": ["root_node", "gen"],
		"target": ["register2", "gen"]
	},
	{
		"origin": ["root_node", "gen"],
		"target": ["register3", "gen"]
	},
	{
		"origin": ["register1", "gen"],
		"target": ["register4", "gen"]
	},
	{
		"origin": ["register1", "gen"],
		"target": ["register5", "gen"]
	},
	{
		"origin": ["register2", "gen"],
		"target": ["register4", "gen"]
	},
	{
		"origin": ["register2", "gen"],
		"target": ["register5", "gen"]
	},
	{
		"origin": ["register2", "gen"],
		"target": ["register6", "gen"]
	},
	{
		"origin": ["register3", "gen"],
		"target": ["register5", "gen"]
	},
	{
		"origin": ["register3", "gen"],
		"target": ["register6", "gen"]
	},
	{
		"origin": ["register4", "gen"],
		"target": ["register7", "gen"]
	},
	{
		"origin": ["register4", "gen"],
		"target": ["register8", "gen"]
	},
	{
		"origin": ["register5", "gen"],
		"target": ["register7", "gen"]
	},
	{
		"origin": ["register5", "gen"],
		"target": ["register8", "gen"]
	},
	{
		"origin": ["register5", "gen"],
		"target": ["register9", "gen"]
	},
	{
		"origin": ["register6", "gen"],
		"target": ["register8", "gen"]
	},
	{
		"origin": ["register6", "gen"],
		"target": ["register9", "gen"]
	},
	{
		"origin": ["register7", "gen"],
		"target": ["exit_node", "gen"]
	},
	{
		"origin": ["register8", "gen"],
		"target": ["exit_node", "gen"]
	},
	{
		"origin": ["register9", "gen"],
		"target": ["exit_node", "gen"]
	}
]

# activation value, root node name, slot name
root_node_data = [1, "root_node", "gen"]

# exit node name, gate name
exit_node_data = ["exit_node", "gen"]
