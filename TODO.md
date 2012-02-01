1. MVP

- basic REST-y framework build on top of twisted.web
- basic validation for input data (argument types, etc.)
- use introspection and magic to build most of the functionality, no copy and paste!
- basic auth mechanism - user sends provider credentials in X header with every request
- for now use threads.deferToThread when calling libcloud methods
- API versioning based on the libcloud release version
- Support for compute API

2. Support for provider specific arguments and methods (ex_foo)

- parse / introspect docstrings to figure out provider specific methods + arguments and their types
- hook it up with the rest of the system
- discovery of provider capabilities through an endpoints

3. Pluggable caching & better auth mechanism

- Pluggable caching system (file, memory, memcache, redis, ...)
- Cache credentials, session id,...
- Cache provider responses

4. Support for other APIs:

- DNS
- Load balancers
- Storage (might be a bit tricky because of upload and download functionality)

5. Other

- auto-generate clients in different languages
- libcloud driver for libcloud.http (meta, baby!)
