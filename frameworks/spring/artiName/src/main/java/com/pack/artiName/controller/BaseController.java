package com.pack.artiName.controller;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.web.bind.annotation.*;

import static org.springframework.web.bind.annotation.RequestMethod.GET;

@RestController
public class BaseController {
    private static final String template = "Hello, %s!";
    private final int a = 0;

    @RequestMapping( path = "/g", method = GET)
    @ResponseBody
    public String greeting(){//@RequestParam(defaultValue = "World") String name) {
        return Integer.toString(a) + String.format(template, "bitch");
    }
    @RequestMapping(value = "/ex", method = RequestMethod.GET)
    public String getFoosBySimplePath() {
        return "Get some Foos";
    }
    @GetMapping("/ge")
    public String getAllStudents() {
        return "studentRepository.findAll()";
    }
}
