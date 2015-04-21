.. _MAP-plugin:

===========
MAP Plugins
===========

.. sectionauthor:: Hugh Sorby

The Plugin lies at the heart of the MAP framework.  The key idea behind the plugins is to make them as simple as possible to implement.  The interface is defined in documentation and the plugin developer is expected to adhere to it.  The framework leaves the responsibility of conforming to the plugin interface up to the plugin developer.  The plugin framework is based on Marty Alchin's [1] article on a plugin framework for Django.  The plugin framework is very lightweight and requires no external libraries and can be made to work with Python 2 and Python 3 simultaneously.


Workflow Step
=============

The Workflow Step is the basic item that a plugin developers need to place their software within.  A workflow step can be of any size and complexity.  Although it must adhere to the plugin design to work properly with the application.  Every step that wishes to act like a Workflow Step must derive itself from the Workflow step mountpoint.  The Workflow step mountpoint is the interface between the application and the plugin.  The Workflow step mountpoint can be imported like so:

::

 from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint

A skeleton step is provided as a starting point for the developer to create their own workflow steps.  The skeleton step is actually a valid step in its own right and it will show up in the Step box if enabled.  However the skeleton step has no use other than as an item to drag around on the workflow area.  The skeleton step is discussed below, before that the plugin interface itself is discussed.

Plugin Interface
----------------

The plugin interface is the layer between the application and the developers plugin.  The plugin interface is not defined by contract as we so often see in Java.  But rather the plugin interface is defined by documentation.  This puts the burden of the specification on the documentation and the conformity of the specification on the developer.  The underlying theory is that the developer is able to follow the specification without the application having to do rigourous checks to make sure this is the case.  The phrase 'If it walks like a duck' is often used.

In this section the specification of the Workflow step plugin interface is given.  It is then upto the developer to make sure their plugin behaves like one.
 
The details of the plugin interface are provided in the documentation of the source code in the relevant source file and additionally here for easy reference.  The documentation provided with the source code is very direct with little explanation the following documentation provides a bit more explanation and discussion on the various aspects of the plugin interface.  The documentation provided here should be considered the slave documentation and the documentation provided with the source code as the master documentation.  

There are essentially, what may be considered, three different levels of the plugin design.

 #. The Musts
 #. The Shoulds
 #. The Coulds
 
Creating a workflow step that satisifies the musts will create an actual workflow step that can be added to the workflow area and interacted with.  But it won't be very useful.  Satisfying the shoulds will usually be sufficient for the very simplest of steps.  Simple steps are for instance ones that provide images, or location information for data.  Doing some of the coulds will create a much more interesting step.

The requirements for creating a step have been kept as simple as possible, this is to allow the developer a quick route into the development of the step content. 

The following three sections discuss these three levels in more detail.

A Step Must
-----------

 * The plugin must be derived from the WorkflowStepMountPoint class defined in the package mapclient.mountpoints.workflowstep
 * Accept a single parameter in it's __init__ method.
 * Define a name for itself, this must be passed into the initialisation of the base class.
 * Define the methods
 
   ::
  
     def configure(self):
         pass
     
     def getIdentifier(self):
         pass
     
     def setIdentifier(self, identifier):
         pass
     
     def serialize(self, location):
         pass
     
     def deserialize(self, location):
         pass
 
A Step Should
-------------
 
 * Implement the configure method to configure the step.  This is typically in the form of a dialog.  When implementing this function the class method self._configuredObserver() should be called to inform the application that the step configuration has finished.
 * Implement the getIdentifier/setIdentifier methods to return the identifier of the step.
 * Implement the serialize/deserialize methods.  The steps should serialize and deserialize from a file on disk located at the given location.
 * Define a class attribute _icon.  That is of the type QtGui.QImage.
 * Information about what the step uses and/or what it provides.  This is achieved through defining ports on the step.
 
A Step Could
------------

 * Implement the method 'setPortData(self, index, dataIn)' if it uses some information from another step.  
 * Implement the method 'getPortData(self, index)' if it was providing some information to another step.
 * Implement the method 'execute(self)' If a step implements the 'execute(self)' method then it must call '_doneExecution()' when the step is finished.
 * Define a category using the '_category' attribute.  This attribute will add the step to the named category in the step box, or it will create the named category if it is not present.
 * Set a widget as the main widget for the MAP Client application.  Calling '_setCurrentWidget(step_widget)' with a widget passed as a parameter will set that widget to the main widget for the MAP Client application.  The widget will be removed when '_doneExecution()' is called.

Pre-defined Step Attributes
---------------------------

A step has a number of pre-defined attributes with default values, they are:

 * self._name = name
 * self._location = location
 * self._category = 'General'
 * self._ports = []
 * self._icon = None
 * self._configured = False

The '_name' and '_location' attributes are passed in to the '__init__' method of the mount point.  The '_category' attribute can be used to group steps in the step box.  By default a step has no ports and at least one port must be defined before it can be used in a workflow.  If the '_icon' attribute is not defined then a default icon is supplied.  The '_configured' property is set to False initially as most steps will not be configured in their initial state.

Pre-defined Step Methods
------------------------

A step has a number of pre-defined methods, they are:

 * execute(self)
     A method that gets called when execution passes to this step.
 * getPortData(self, index)
     A method that returns the object that is defined by the port for the given index of the step 
 * setPortData(self, index, dataIn)
     A method that sets the ports data for the given index.
 * configure(self)
     A method called by the framework to inform the step that it needs to follow it's configuration procedure. 
 * isConfigured(self)
     A method to return the value of '_configued'.  In most cases this method will not 
     need to be overridden.
 * _configuredObserver
     A method to call to let the framework know that the step configuration has finished.
 * _identifierOccursCount
     A method to call to determine the number of identifiers with the given value.  This method can be used to decide whether the current identifier is unique across the workflow.
 * addPort
     Adds a port to the step, the port is defined using an RDF triple.  See the
     Ports section for more information.
 * getName(self)
     Returns the '_name' attribute if it is set otherwise returns the class name.  In most cases this method will not 
     need to be overridden.
 * deserialize(self, location)
     Must be implemented in the plugin otherwise an exception is raised. 
 * serialize(self, location)
     Must be implemented in the plugin otherwise an exception is raised. 
 * _setCurrentWidget(step_widget)
     Set widget 'step_widget' to the main widget for the framework.
 * _doneExecution()
     Inform the framework that the step has finished it's task.
 * registerDoneExecution(self, observer)
     A method used by the framework to set the callable when execution is done.  This method should not be overwritten.
 * registerOnExecuteEntry(self, observer, undoRedoObserver)
     A method used by the framework to set a callable to set up the step for execution.  This method should not be overwritten.
 * registerConfiguredObserver(self, observer)
     A method used by the framework to set a callable for notifying when the step has been configured.  This method should not be overwritten.
 * registerIdentifierOccursCount
     A method used by the framework to set a callable for determining the number of times the given identifier occurs in the current workflow.  This method should not be overwritten.

Ports
=====

A port is a device to specify what a workflow step provides or uses.  A port is described using Resource Description Framework (RDF) triples.  The port description is used to determine whether or not two ports may be connected together.
One port can either use or provide one thing. A single port must not both provide a thing and use a thing.  Ports are ordered by entry position.

A port is defined with the subject of *http://physiomeproject.org/workflow/1.0/rdf-schema#port* and it can be defined with a property or characteristic as either providing (*http://physiomeproject.org/workflow/1.0/rdf-schema#provides*) or using (*http://physiomeproject.org/workflow/1.0/rdf-schema#uses*) an object.  What that object is is defined by the step, for example the image source step defines the following port:

  (http://physiomeproject.org/workflow/1.0/rdf-schema#port, http://physiomeproject.org/workflow/1.0/rdf-schema#provides, http://physiomeproject.org/workflow/1.0/rdf-schema#images)

Any step that understands the *http://physiomeproject.org/workflow/1.0/rdf-schema#images* object can define it's own port that uses this object.  Ports are added to a step by using the 'addPort(self, triple)' method from the base class.

Skeleton Step
=============

The skeleton step satisfies the musts of the plugin interface.  It is a minimal step and it is set out as follows.

A Python package with the step name is created, in this case 'skeletonstep',  in the module file we add the code that needs to be read when the plugins are loaded.

The module file performs four functions.  It contains the version information and the authors name of the module.  For instance the skeleton step has a version of '0.1.0' and authors name of 'Xxxx Yyyyy'.  It adds the current directory into the Python path, this is done so that the steps python files know where they are in relation to the python path.  It also (optionally) prints out a message showing that the plugin has been loaded successfully.  But the most important function it performs is to call the python file that contains the class that derives from the workflow step mountpoint.

The 'SkeletonStep' class in the skeletonstep.step package is a very simple class.  It derives from the 'WorkflowStepMountPoint', calls the base class with the name of the step, accepts a single parameter in it's init method and defines the five required functions to satisfy the plugin interface.

When enabled the skeleton step will be a fully functioning step in the MAP Client.

References
==========

[1] http://martyalchin.com/2008/jan/10/simple-plugin-framework/ Marty Alchin on January 10, 2008