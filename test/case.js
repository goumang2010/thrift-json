var thriftToJSON =require('../index.js');
thriftToJSON(`./test/storm.thrift`)
.then(res => console.log(res));