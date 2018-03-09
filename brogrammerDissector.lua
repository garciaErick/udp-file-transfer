-- adrian protocol example
-- author: Adrian Veliz (Original Code)
-- author: Erick Garcia
-- author: Fernando Martinez


local adrian_proto = Proto("brocode","Bro Code")

-- create a function to dissect it
function adrian_proto.dissector(buffer,pinfo,tree)
    pinfo.cols.protocol = "BROCODE"
    local subtree = tree:add(adrian_proto,buffer(),"BroCode Protocol Data")

	-- Message is at least three bytes long
	if buffer:len() < 3 then
		subtree:add_expert_info(PI_MALFORMED, PI_ERROR, "Invalid Message")
		return end
	
	-- All messages have a sequence number and type
    local seq_num = buffer(0,1):uint()
    local msg_type = buffer(1,1):string() 
    local command = buffer(0,3):string()
    local fullMessage = buffer():string()
    
    subtree:add(buffer(0,1),"Sequence Number: " .. seq_num)
    subtree:add(buffer(1,1),"Type: " .. msg_type)
    subtree:add(buffer(0,3),"command: " .. command)
    subtree:add("Full Message: " .. fullMessage)

    if command == "GET" or command == "PUT" then -- Request a file
	myProtocol =  command
	subtree:add(buffer(2), "FILE: " .. buffer(3):string())
    elseif fullMessage == "Received last packet" or "Finished!" then -- Request a file
	subtree:add("Finished " .. myProtocol .. " request")
    else						-- Unknown message type	
        subtree:add_expert_info(PI_PROTOCOL, PI_WARN, "Unknown message type")
        subtree:add(buffer(0),"ERROR: " .. buffer(0))
    end
end
-- load the udp.port table
udp_table = DissectorTable.get("udp.port")
tcp_table = DissectorTable.get("tcp.port")
-- register protocol to handle udp ports
udp_table:add(5000,adrian_proto)
udp_table:add(5001,adrian_proto) 
udp_table:add(5002,adrian_proto)
udp_table:add(50000,adrian_proto)
udp_table:add(50001,adrian_proto)
udp_table:add(50002,adrian_proto)
tcp_table:add(5000,adrian_proto)
 
-- original source code and getting started
-- https://shloemi.blogspot.com/2011/05/guide-creating-your-own-fast-wireshark.html

-- helpful links
-- https://delog.wordpress.com/2010/09/27/create-a-wireshark-dissector-in-lua/
-- https://wiki.wireshark.org/LuaAPI/Tvb
-- http://lua-users.org/wiki/LuaTypesTutorial
-- https://wiki.wireshark.org/Lua/Examples
-- https://wiki.wireshark.org/LuaAPI/Proto
-- https://www.wireshark.org/docs/wsdg_html_chunked/wslua_dissector_example.html
-- https://www.wireshark.org/lists/wireshark-users/201206/msg00010.html
-- https://wiki.wireshark.org/LuaAPI/TreeItem
-- https://www.wireshark.org/docs/man-pages/tshark.html

