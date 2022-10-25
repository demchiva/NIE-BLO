# Semestral work - implementation of D21 voting method

"Janečkova metoda D21" is a modern voting system, which allows more accurate voting. You can learn more about it here: https://www.ih21.org/o-metode. In our exercise, we want to achieve the following use cases:

UC1 - Everyone can register a subject (e.g. political party)
UC2 - Everyone can list registered subjects
UC3 - Everyone can see the subject’s results
UC4 - Only the owner can add eligible voters
UC5 - Every voter has 2 positive and 1 negative vote
UC6 - Voter can not give more than 1 vote to the same subject
UC7 - Negative vote can be used only after 2 positive votes
UC8 - Voting ends after 7 days from the contract deployment

## Interface

This interface will help you with the contract implementation. It is necessary to strictly follow this interface and naming for the successful evaluation of the final exercise.

```
// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

interface IVoteD21{

}
```

## Subject structure

Define the structure inside the interface. The subject of voting can be for example a political party.

```
struct Subject{
    string name;
    int votes;
}
```

## Interface functions

Add a new subject into the voting system using the name.

```
function addSubject(string memory name) external;
```

Add a new voter into the voting system.

```
function addVoter(address addr) external;
```

Get addresses of all registered subjects.

```
function getSubjects() external view returns(address[] memory);
```

Get the subject details.

```
function getSubject(address addr) external view returns(Subject memory);
```

Vote positive for the subject.

```
function votePositive(address addr) external;
```

Vote negative for the subject.

```
function voteNegative(address addr) external;
```

Get the remaining time to the voting end in seconds.

```
function getRemainingTime() external view returns(uint);
```

Get the voting results, sorted descending by votes.

```
function getResults() external view returns(Subject[] memory);
```

## Create the contract

Now we create the contract, which implements the defined interface.

```
pragma solidity 0.8.9;

import "./IVoteD21.sol";

contract D21 is IVoteD21 {

}
```

## Implement the logic

Implementation of the smart contract completely depends on you. There are many possible ways how to achieve it. The only important thing is, to follow the IVoteD21 interface. If you have any blocker or questions, don’t hesitate to ask.

## Implementation
* 20 points (all the use cases must be implemented correctly, and all our tests must pass)
Unit tests
* 10 points (10 points for unit tests with full coverage)
* Gas optimizations - 10 points (make your contract as efficient as possible, will be compared to reference implementation)

## Testing framework

The tests should be implemented in the Brownie testing framework https://eth-brownie.readthedocs.io/en/stable/. Brownie will be discussed in the upcoming tutorials.


## Resources

The following resources were used for creating this tutorial. The italicized text is slightly modified text from those sources. They are recommended for further reading.

* Solidity documentation (https://docs.soliditylang.org/en/v0.8.17/#contents)
    * contents of the official Solidity documentation
* Mastering Ethereum, chapter on EVM (https://github.com/ethereumbook/ethereumbook/blob/develop/13evm.asciidoc)
    * free book about Ethereum with a good chapter on EVM
* Ethereum Yellow Paper (https://ethereum.github.io/yellowpaper/paper.pdf)
    * official Ethereum specification
* More accessible interpretation of the Yellow Paper (https://ethereum.org/en/developers/tutorials/yellow-paper-evm/#main-content)
* EVM Opcodes (https://www.evm.codes/)
interactive EVM opcodes reference
* Introduction to smart contracts https://docs.soliditylang.org/en/latest/introduction-to-smart-contracts.html#introduction-to-smart-contracts)
    * introduction to smart contracts from solidity documentation