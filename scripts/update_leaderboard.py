import json
import os
from github import Github  # PyGithub 库

# 从环境变量获取 GitHub Token
GITHUB_TOKEN = os.getenv("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")
REPO_NAME = "barbatoswang/scordlist"  # 替换为你的仓库


def update_leaderboard():
    # 1. 读取现有排行榜
    with open("dosc/leaderboard.json", "r") as f:
        leaderboard = json.load(f)

    # 2. 获取最新的 Issue（成绩提交）
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    issues = repo.get_issues(state="open")  # 获取所有未关闭的 Issue

    for issue in issues:
        if "[Score]" in issue.title:
            # 解析玩家和成绩（示例标题：[Score] PlayerName: 100）
            try:
                _, player, score = issue.title.split()
                player = player.rstrip(":")  # 移除冒号
                score = int(score)

                # 3. 添加到排行榜
                leaderboard.append({"player": player, "score": score})

                # 4. 关闭 Issue（避免重复处理）
                issue.edit(state="closed")
            except (ValueError, IndexError):
                print(f"忽略无效 Issue: {issue.title}")

    # 5. 按分数排序并保存
    leaderboard.sort(key=lambda x: -x["score"])
    with open("dosc/leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=2)


if __name__ == "__main__":
    update_leaderboard()
