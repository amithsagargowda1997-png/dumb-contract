// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Bank {
    mapping(address => uint) balances;

    function withdraw() public {
        uint amount = balances[msg.sender];
        _send(msg.sender, amount);
        balances[msg.sender] = 0;
    }

    function _send(address to, uint amount) internal {
        (bool ok, ) = to.call{value: amount}("");
        require(ok);
    }
}
