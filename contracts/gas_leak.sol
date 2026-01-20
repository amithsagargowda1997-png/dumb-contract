// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GasDOS {
    address[] users;

    function payout() public {
        for (uint i = 0; i < users.length; i++) {
            payable(users[i]).call("");
        }
    }
}
