from db import get_all_voters

def generate_report():
    voters = get_all_voters()

    total_registered = len(voters)
    voted = sum(1 for _, _, _, has_voted in voters if has_voted)

    print("📊 ELECTION REPORT")
    print("------------------")
    print(f"Total Registered Voters: {total_registered}")
    print(f"Votes Cast: {voted}")
    print(f"Pending Votes: {total_registered - voted}")

if __name__ == "__main__":
    generate_report()
