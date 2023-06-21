-- Chisel description
description = "count syscalls executed over a time period in json format";
short_description = "syscall count";
category = "misc";

-- Chisel argument list
args = {}


function on_init()
	
	chisel.set_filter("not (evt.type in ('switch', 'scapevent', 'useradded'," ..
		"'groupadded', 'userdeleted', 'groupdeleted', 'pluginevent', 'container'," ..
		"'page_fault', 'infra', 'notification', 'mesos', 'tracer', 'k8s', 'cpu_hotplug'," ..
		"'signaldeliver', 'drop', 'getcwd')) and evt.dir='>'")
	return true
end

syscall_count = {}


-- Event parsing callback
function on_event()

	local eType = evt.get_type()

	if syscall_count[eType] == nil then		
		syscall_count[eType] = 1
	else
		syscall_count[eType]= syscall_count[eType] + 1
	end
	
	return true
end

function on_capture_end()
	print("{")
	for k,v in pairs(syscall_count) do
		print('"' .. k .. '" : ' .. v .. ',')
	end
	print("}")
	return true
end


