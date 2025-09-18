package com.pack.artiName.websockets;


import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;

@Controller
public class WebSocketController {

    @MessageMapping("/chat.send")     // listens on /app/chat.send
    @SendTo("/topic/messages")        // sends to /topic/messages
    public ChatMessage sendMessage(ChatMessage message) {
        return message; // echoes back the received message
    }
}