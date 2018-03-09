-- Brocode Protocol
-- author: Adrian Veliz (Original Code)
-- author: Erick Garcia
-- author: Fernando Martinez


local brocode_proto = Proto("brocode","Bro Code")

-- create a function to dissect it
function brocode_proto.dissector(buffer,pinfo,tree)
    pinfo.cols.protocol = "BROCODE"
    local subtree = tree:add(brocode_proto,buffer(),"BroCode Protocol Data")

	-- Message is at least three bytes long
	if buffer:len() < 3 then
		subtree:add_expert_info(PI_MALFORMED, PI_ERROR, "Invalid Message")
		return end
	
	-- All messages have a sequence number and type
    local seq_num = buffer(0,1):uint()
    local msg_type = buffer(1,1):string() 
    local command = buffer(0,3):string()
    local fullMessage = buffer():string()
    unknownMessage = false
    

    if command == "GET" or command == "PUT" then -- Request a file
	myProtocol =  command
	myFile = buffer(3):string()
	myStatus = "Innitiating protocol"
    elseif fullMessage == "Received last packet" or fullMessage == "Finished!" then -- Request a file
	myStatus = "Finished " .. myProtocol .. " request"
    elseif fullMessage == "Acknowledging handshake from server" then -- Request a file
	myStatus = "Started Communication"
    elseif string.match(fullMessage,"Recieved packet") then -- Request a file
	myStatus = "Recieved packet " .. fullMessage:sub(17,17)
    else --Unkown message, do not print Protocol || File || Status
	subtree:add("Probably processing file...")
        subtree:add_expert_info(PI_PROTOCOL, PI_WARN, "Unknown message type")
        subtree:add(buffer(0),"ERROR: " .. buffer(0))
	unknownMessage  = true
    end
    if unknownMessage  == false then --Valid message, print everything 
	subtree:add("Protocol: " .. myProtocol)
	subtree:add("FILE: " .. myFile)
	subtree:add("STATUS: " .. myStatus)
    end
end
-- load the udp.port table
udp_table = DissectorTable.get("udp.port")
-- register protocol to handle udp ports
udp_table:add(50000,brocode_proto)
udp_table:add(50001,brocode_proto)
udp_table:add(50002,brocode_proto)
 
