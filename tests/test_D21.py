import pytest
from brownie import chain, D21, accounts, reverts

@pytest.fixture
def contract():
    return D21.deploy({'from': accounts[0]})

def testOwnerAndDeadline(contract: D21):
    assert contract.owner() == accounts[0]

def testAddSubject(contract: D21):
    contract.addSubject("sub1", {'from': accounts[1]})
    with reverts("One person can create one subject only. You have already created one."):
        contract.addSubject("sub2", {'from': accounts[1]})

def testAddVoter(contract: D21):
    with reverts("Contract owner only can add voters."):
        contract.addVoter(accounts[2], {'from': accounts[1]})

    contract.addVoter(accounts[2], {'from': accounts[0]})

    with reverts("This person was already added as a voter."):
        contract.addVoter(accounts[2], {'from': accounts[0]})

def testGetSubjects(contract: D21):
    contract.addSubject("sub1", {'from': accounts[1]})
    assert contract.getSubjects() == [accounts[1]]

    contract.addSubject("sub2", {'from': accounts[2]})
    assert contract.getSubjects() == [accounts[1], accounts[2]]

def testGetSubject(contract: D21):
    contract.addSubject("sub1", {'from': accounts[1]})
    contract.addSubject("sub2", {'from': accounts[2]})

    subject1 = contract.getSubject(accounts[1])
    assert subject1["name"] == "sub1"

    subject2 = contract.getSubject(accounts[2])
    assert subject2["name"] == "sub2"

def testVotePositive(contract: D21):
    contract.addVoter(accounts[2], {'from': accounts[0]})

    with reverts("Subject does not exist."):
        contract.votePositive(accounts[0], {'from': accounts[2]})

    contract.addSubject("sub1", {'from': accounts[1]})

    with reverts("You can not vote."):
        contract.votePositive(accounts[1], {'from': accounts[0]})

    contract.votePositive(accounts[1], {'from': accounts[2]})
    subject1 = contract.getSubject(accounts[1])
    assert subject1["votes"] == 1

    with reverts("You have already voted for this subject."):
        contract.votePositive(accounts[1], {'from': accounts[2]})

    contract.addVoter(accounts[1], {'from': accounts[0]})
    contract.votePositive(accounts[1], {'from': accounts[1]})
    subject1 = contract.getSubject(accounts[1])
    assert subject1["votes"] == 2

    contract.addSubject("sub2", {'from': accounts[0]})
    contract.addSubject("sub3", {'from': accounts[2]})
    
    contract.votePositive(accounts[0], {'from': accounts[2]})
    subject1 = contract.getSubject(accounts[0])
    assert subject1["votes"] == 1

    with reverts("You have already dive positive vote twice."):
        contract.votePositive(accounts[0], {'from': accounts[2]})


def testVoteNegative(contract: D21):
    contract.addVoter(accounts[2], {'from': accounts[0]})

    with reverts("Subject does not exist."):
        contract.voteNegative(accounts[0], {'from': accounts[2]})

    contract.addSubject("sub1", {'from': accounts[1]})

    with reverts("You can not vote."):
        contract.voteNegative(accounts[1], {'from': accounts[0]})

    with reverts("You must vote positive twice, before vote negative."):
        contract.voteNegative(accounts[1], {'from': accounts[2]})

    contract.addSubject("sub2", {'from': accounts[0]})
    contract.addSubject("sub3", {'from': accounts[2]})
    contract.addSubject("sub4", {'from': accounts[3]})

    contract.votePositive(accounts[0], {'from': accounts[2]})
    contract.votePositive(accounts[2], {'from': accounts[2]})

    with reverts("You already voted positive for this subject"):
        contract.voteNegative(accounts[0], {'from': accounts[2]})
    
    contract.voteNegative(accounts[1], {'from': accounts[2]})

    with reverts("You have already voted negative."):
        contract.voteNegative(accounts[3], {'from': accounts[2]})

def testGetRemainingTime(contract: D21):
    remainingTime = contract.getRemainingTime()
    oneWeekInSeconds =  60 * 60 * 24 * 7
    assert remainingTime == oneWeekInSeconds
    sleep_time = 31337
    chain.sleep(sleep_time)
    chain.mine()
    remainingTime = contract.getRemainingTime()
    assert remainingTime == oneWeekInSeconds - sleep_time

def testGetResults(contract: D21):
    contract.addSubject("sub0", {'from': accounts[0]})
    contract.addSubject("sub1", {'from': accounts[1]})
    contract.addSubject("sub2", {'from': accounts[2]})

    contract.addVoter(accounts[0], {'from': accounts[0]})
    contract.addVoter(accounts[1], {'from': accounts[0]})
    contract.addVoter(accounts[2], {'from': accounts[0]})

    contract.votePositive(accounts[1], {'from': accounts[0]})

    contract.votePositive(accounts[1], {'from': accounts[1]})
    contract.votePositive(accounts[2], {'from': accounts[1]})

    contract.votePositive(accounts[1], {'from': accounts[2]})
    contract.votePositive(accounts[2], {'from': accounts[2]})

    contract.voteNegative(accounts[0], {'from': accounts[2]})

    results = contract.getResults()
    assert results == (('sub1', 3), ('sub2', 2), ('sub0', -1))