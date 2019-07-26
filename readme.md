# I3CM 

High level arcithecture of the I3CM software.  

Given the fact that the software will be run on a Beagle the soft is separated so that a server can be ran on the beeagle or whatever PC talking to devices and a client can be ran on a distant PC. 

The whole system desciption is done with configuration files in yaml langage. These configuration are red and wrote inside a simple, flat, database. The database is only key/values pairs that can be mirrored by any client. The idea is that the whole system configuration and state is inside the database. 

A set of key/value pair with the same root and `root.type` is defining a database :

```python 
{ 
I3CM.MOTORS.MOTOR1.CURRENT.type : "parameter", 
I3CM.MOTORS.MOTOR1.CURRENT.ptype : "float",
I3CM.MOTORS.MOTOR1.CURRENT.desciption : "motor current consumption" ,
I3CM.MOTORS.MOTOR1.CURRENT.unit : "A"
}
```
here `I3CM.MOTORS.MOTOR1.CURRENT` point must be interpreted as a `paramter` type. 

There are several types for the database they are explain bellow 

parameter
---------

A parameter is basicaly a value join with description unit, etc, but also parsing rules to make sure that the input value is always appropriate. For instance:

```yaml
SUBSTATE:   
    type: parameter
    ptype: [str, listed]
    list: [MOVING, IDL, ERROR]                
    description: Motor sub state
```

Is a string listed, only 'MOVING', 'IDL' or 'ERROR' can be accepted.

An other exemple :

```yaml
BIT_ADDRESS:
    type: parameter
    ptype: [int, bounded]
    min: 0
    max: 3
    description: Motor bit address (2 bits) 
```

Is an integer bounded between 0 and 3. 

Accpeted parser are indicated in the table bellow

| ptype   | needed properties | comment                                       |
| ------- | ----------------- | --------------------------------------------- |
| str     |                   | parse input as str                            |
| float   |                   | parse input as float                          |
| int     |                   | parse input as integer                        |
| bool    |                   | parse input as integer boolean                |
| listed  | list              | input must be on list                         |
| bounded | min, max          | input must be between min and max             |
| clipped | min, max          | every input <min will be min >max will be max |


system
------

represent a group of parameter and device. a System is suppose to have a python process function counterpart and eventually a thread running that will update the hardware state inside the database. A system can accept parameters, devices, and commands. 

 





 


