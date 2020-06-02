// Reference 
// https://github.com/angelol/eos-keygen

const ecc = require('eosjs-ecc')

function generate() {
  var eccj = ecc;

  eccj.randomKey().then(function (value) {
    var pubkey = eccj.privateToPublic(value)

    console.log(value)
    console.log(pubkey)

  })
}
generate()


