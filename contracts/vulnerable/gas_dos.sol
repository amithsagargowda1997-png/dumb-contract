// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GasDOS {
    address[] public users;

    function addUser(address user) public {
        users.push(user);
    }

    function payout() public {
        for (uint256 i = 0; i < users.length; i++) {
            // Unbounded loop + external call
            payable(users[i]).call("");
        }
    }
}
