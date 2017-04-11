# self-python-sdk

This is the Intu SDK written in Python. The SDK is a thin WebSocket-based client that lets users make
WebSocket connections to a running Intu instance, as well as create their own custom gestures, sensors, and
agents that they can then plug in into the system. The whole system follows the publish-subscribe pattern.

1) Requirements

Need ws4py installed (pip install ws4py)

2) How to test

Run $ python test_topic_client.py

2) Notes

The following warning has been observed on Mac El Capitan OS:

UserWarning: You do not have a working installation of the service_identity module: 'No module named service_identity'. Please install it from <https://pypi.python.org/pypi/service_identity> and make sure all of its dependencies are satisfied. Without the service_identity module, Twisted can perform only rudimentary TLS client hostname verification. Many valid certificate/hostname mappings may be rejected.

WARNING: 140: This application, or a library it uses, is using the deprecated Carbon Component Manager for hosting Audio Units. Support for this will be removed in a future release. Also, this makes the host incompatible with version 3 audio units. Please transition to the API's in AudioComponent.h.
