package com.plobber.routing.graphhopper;

import com.graphhopper.json.Statement;
import com.graphhopper.json.Statement.Op;
import com.graphhopper.util.CustomModel;
import org.springframework.stereotype.Component;

@Component
public class CustomModelBuilder {

    public CustomModel build(String mode) {
        CustomModel model = new CustomModel();

        if ("PLOGGING".equalsIgnoreCase(mode)) {
            model.addToPriority(Statement.If("trash_prob < 0.3", Op.MULTIPLY, "0.2"));
            model.addToPriority(Statement.ElseIf("trash_prob < 0.6", Op.MULTIPLY, "0.5"));
        } else if ("COMFORT".equalsIgnoreCase(mode)) {
            model.addToPriority(Statement.If("trash_prob > 0.8", Op.MULTIPLY, "0.1"));
            model.addToPriority(Statement.ElseIf("trash_prob > 0.5", Op.MULTIPLY, "0.5"));
        }

        return model;
    }
}
