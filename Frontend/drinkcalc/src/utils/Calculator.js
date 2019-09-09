class Utility {
    calculateAlcoholConsumed(alcoholPercent, volume) {
        grossAlcohol = (alcoholPercent / 100) * volume;
        netAlcohol = grossAlcohol * 0.8;
    }

    calculateBAC(alcoholConsumed, bodyWeight, gender, time) {
        if (gender == 'm') {
            r = 0.68;
            bloodAlcohol = (((alcoholConsumed /
                (bodyWeight * r)) * 100) - (0.015 * time))
            return bloodAlcohol
        }
        else if (gender == 'f') {
            r = 0.55;
            bloodAlcohol = (((alcoholConsumed /
                (bodyWeight * r)) * 100) - (0.015 * time))
            return bloodAlcohol
        }
        else {
            return 0
        }
    }
}