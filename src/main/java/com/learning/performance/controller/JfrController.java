package com.learning.performance.controller;

import com.learning.performance.service.JfrService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.MalformedURLException;
import java.nio.file.Path;

@RestController
@RequestMapping("/api/recording")
public class JfrController {

    @Autowired
    private JfrService jfrService;

    @PostMapping("/start")
    public String start() {
        jfrService.startRecording();
        return "Recording Started";
    }

    @PostMapping("/stop")
    public ResponseEntity<Resource> stopAndDownload() {
        Path path = jfrService.stopRecording();
        try {
            Resource resource = new UrlResource(path.toUri());
            return ResponseEntity.ok()
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .header(HttpHeaders.CONTENT_DISPOSITION,
                            "attachment; filename=\"" + path.getFileName().toString() + "\"")
                    .body(resource);
        } catch (MalformedURLException e) {
            return ResponseEntity.internalServerError().build();
        }
    }
}
