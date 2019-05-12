![PROTON Logo](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON-logo.png)
# PROTON
**The MIC stack genesis!**

PROTON is a high-level Python framework that facilitates rapid server-side development with clean & pragmatic design. 
Thanks for checking it out!

- PROTON aims at easing server-side development for all Python enthusiasts. 
- With PROTON, as a developer you issue **one command**; 
one command, to spin up auto generated code with pragmatic separation of Model, Controller and Interface 
<small>(Hence the name, MIC stack)</small>! 
- One command to setup a production ready server side stack with managed DB connections <small>(PROTON ships with postgresql)</small>, 
managed caching <small>(PROTON ships with redis)</small>, descriptive logging and auto-generated openAPI specs.
- All of this, is **containerised**!

# Getting Started
- Install docker on your development machine. 
    - Linux - https://docs.docker.com/install/linux/docker-ce/ubuntu/
    - Mac - https://docs.docker.com/docker-for-mac/install/
    - Windows - https://docs.docker.com/docker-for-windows/install/
- Clone PROTON to your desired location `git clone https://github.com/PruthviKumarBK/PROTON.git`
- Change directory to PROTON `cd ~/PROTON/`
- `./cproton.sh -U yes` PROTON will ask your input for few key environment variables.
- Wait for the platform to bootstrap; once **done**, visit `http://localhost:3000`. 
- Congratulations. you've got your server-side setup!

# Example

Generate a new MIC stack named **testMic** :
`
 ./protongen.sh -n testMic -p 3000
`

![PROTON MIC stack for testMic](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_testMic.png)

Your code base will now include, dynamically generated content for **testMic** all the way from Model, Controller & Interface!

![PROTON MIC stack for testMic](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_stack_testMic.png)

PROTON will dynamically generate an API for every method defined in the controller for **testMic**. Right now, there is a method named `schemaInformation` within `controller_testMic.py` for **testMic**. Convention for generated route will be <get_micName_controllerMethod>. Go to, `localhost:3000/get_testMic_schemaInformation`; you will see the schema information for connected database in postgresql! This is the default code auto-generated by PROTON for every new MicStack

![PROTON MIC stack API](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_API_testMic.png)

![PROTON MIC stack API for testMic](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_testMic_schemaInformation.png)

For every auto generated route, cache will steer PROTON on steroids for subsequent get calls! Each entry in cache will live upto a day! You can change this lifespan by editing `CACHE_LIFESPAN` within PROTON's `configuration.py`

![PROTON MIC stack API Cache](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_testMic_cacheSet.png)

![PROTON MIC stack Cache](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_cacheService.png)

Now, when you want to add a new method/expose newer APIs within **testMic**, all you should be doing is write SQL and create a method within PROTON's respective MIC stack.

![PROTON MIC Adding Newer Methods](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_newerMethodsToController.png)

With newer method now in place, to generate API, all you do is issue this one command:
` ./protongen.sh -s yes`

![PROTON MIC NewMethod API](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_updatedWithNewerMethods.png)

Newly generated route will also get cache settled!

![PROTON MIC NewMethod at root](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_newerMethodsOnRoot.png)

![PROTON MIC Cache for NewMethod](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_cacheForNewMethod.png)

![PROTON MIC Cache for NewMethod](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_activeCacheForNewMethod.png)

Generating a new MIC stack will leave existing stack unaltered.

![PROTON MIC generating new stack](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_newMicStack.png)

![PROTON MIC NewMethod at root](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_rootAfterNewMic.png)

Trace for PROTON stack will be enabled throughout. Checkout `./trace/` directory.

![PROTON Trace](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_traceDirectory.png)

![PROTON Trace Logs](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_TraceExample.png)

PROTON also ships with ability to automagically generate OpenAPI specs!

![PROTON OpenAPI](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_OpenApi_directory.png)

![PROTON OpenAPI](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_swagger.yaml.png)

Should you want to delete from existing PROTON MIC stack, you stand one command away! Like Generator, PROTON also ships with Destroyer which pragmatically clears the desired MIC from PROTON stack. (This will also clean the Cache entries automagically; only for mic that is targeted to be killed.)

`./protonkill.sh -k <micName>`

![PROTON destroyer](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_afterKilling_testMic.png)

PROTON will continue to perform/live with remaining MIC stack after destroyer completing its job!

![PROTON After destruction of testMic](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_stackAfterKillingTestMic.png)



NOTE: PROTON uses Gunicorn as High Performance Server. Gunicorn is built to utilize kernel features of Unix/Linux machines. Hence, PROTON will be seamless on Unix/Linux platforms. On Windows, PROTON will require fallback to another WSGI server which is Work In Progress at this moment.

# Features in active development:
- Support for MySql, SqlLite and SqlServer relational databases.
- Pipelines to transfer form and to datawarehouse to database. Support for GCP's bigQuery and AWS's RedShift in progress.
- containerization of PROTON. Docker build and Kubernetes deployable PROTON!
- Auto generated Swagger UI from PROTON generated openAPI specs.

# Support
For any  feedback or issues write to Pruthvi @ pruthvikumar.123@gmail.com. Ensure to have a valid subject line, detailed message with appropriate stack trace to expect prompt/quick response.

# Tags
0.0.1 - PROTON confirms to PEP8 standards.

0.0.2 - Cache is unique not only per route but to query params per route.
# License

BSD 3-Clause License

Copyright (c) 2018, Pruthvi Kumar
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.