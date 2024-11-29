# AD Converter PCF8591 for Raspberry Pi

## Intro
Have you ever wondered how to measure battery voltage with Raspberry Pi? Do not wonder more. You can simply use ADC converter for 2 USD on Ebay with product name PCF8591 and connect it using I2C to your Raspberry Pi.

## How it works?
Basically AD convertor take Vcc voltage as reference, measure input voltage to this reference and output number of how many percent of reference voltage is input voltage. Eg. if you use Raspberry Pi and provide Vcc at 3.3V and input voltage would be 3.3V, output from ADC would be 1.00. If input voltage for same reference would be 1.65V, output from ADX would be 0.50 (input voltage is half of reference voltage).

But usually we need to measure higher voltages than 3.3V. For example in my case I need to measure Lead-Acid battery which provides voltage between 11-14V. So how to solve it if the reference voltage is only 3.3V and anything higher would not be able to be measured. In this case we use voltage divider (see image below) which divide input voltage 6 times. So for example for 12V output voltage would be 12V/6 => 2V and this could be measured. We can easily get input voltage on Raspberry Pi using simple mathematical operation percentage * 3.3V (Vcc) * 6 (divider) and now we will get 12V again on screen.

As you can see on image below I use trimr and voltmeter to calibrate AD converter with computer.

## How to calibrate it
Please use Voltage Divider Calculator ( http://www.daycounter.com/Calculators/Voltage-Divider-Calculator.phtml ) to get values of resistors you need. I strongly recommend you to replace one resistor with trimmer resistor to calibrate it to right value.

For measuring voltage the best is to use quick2wire ( https://github.com/quick2wire/quick2wire-python-api ) api library combined it with my prepared example https://github.com/koss822/misc/blob/master/ad_pcf8591/pcf8591read which has these options:

```
ref_voltage = 3.3
divider = 6
```
where ref_voltage is standard Raspberry Pi 3.3 voltage and divider is voltage divider you selected on calculator above (in my example it is 6)
