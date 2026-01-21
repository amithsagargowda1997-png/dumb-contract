// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Reentrant {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");

        // INTERACTION before EFFECT (vulnerable)
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok);

        balances[msg.sender] = 0;
    }
}
