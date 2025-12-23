import sys
import os
import subprocess
import datetime
import re
import json
from github import Github, Auth
from collections import defaultdict

def run_git_command(repo_path, args):
    """Gitコマンドを安全に実行し、結果をリストで返す"""
    try:
        cmd = ["git", "-C", repo_path] + args
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    except Exception:
        return []

def get_remote_repo_name(repo_path):
    """ローカルパスからGitHubの 'owner/repo' 名を取得する"""
    remotes = run_git_command(repo_path, ["remote", "-v"])
    for line in remotes:
        if "(fetch)" in line:
            match = re.search(r'github\.com[:/](.+?)(?:\.git)?(?:\s|$)', line)
            if match: return match.group(1).strip()
    return "unknown/unknown"

def extract_domain(email):
    """メールアドレスから組織ドメインを抽出（一般的なプロバイダは除外）"""
    if not email or '@' not in email: return None
    domain = email.split('@')[-1].lower()
    ignored = ["gmail.com", "outlook.com", "users.noreply.github.com", "hotmail.com", "icloud.com", "yahoo.co.jp", "me.com"]
    return None if domain in ignored else domain

def main():
    # 1. 環境準備
    token = os.environ.get("GIT_TOKEN_CLASSIC")
    if not token: sys.exit("Error: 環境変数 'GIT_TOKEN_CLASSIC' を設定してください。")
    
    if len(sys.argv) < 2:
        sys.exit("Usage: python chaoss_final_master_fixed.py <local_repo_path> [start_year]")

    local_path = sys.argv[1]
    repo_full_name = get_remote_repo_name(local_path)
    current_year = datetime.datetime.now().year
    
    # 開始年の設定（指定がない場合は2年前から）
    start_year = int(sys.argv[2]) if len(sys.argv) >= 3 else current_year - 2

    yearly_stats = defaultdict(lambda: {
        "commit_counts": defaultdict(int),
        "org_commit_counts": defaultdict(int),
        "total_commits": 0,
        "new_issues": 0, "closed_issues": 0,
        "pr_durations": []
    })

    print(f"--- Analyzing {repo_full_name} since {start_year} ---")
    
    # 2. ローカルGit解析 (コミット・貢献者・組織)
    print("Step 1: Analyzing local git logs...")
    # 指定した開始年より少し前から取得（端境期対策のため広めに取得し、後のループで正確にフィルタ）
    log_data = run_git_command(local_path, ["log", f"--since={start_year}-01-01", "--pretty=format:%aI|%aN|%aE"])
    
    for line in log_data:
        if not line: continue
        parts = line.rsplit('|', 2) # パイプ記号が含まれる名前対策
        if len(parts) < 3: continue
        dt, name, email = parts
        yr = int(dt[:4])
        
        yearly_stats[yr]["total_commits"] += 1
        yearly_stats[yr]["commit_counts"][name] += 1
        org_domain = extract_domain(email)
        if org_domain:
            yearly_stats[yr]["org_commit_counts"][org_domain] += 1

    # 3. GitHub API解析 (Issue/PR と クローズ時間)
    print("Step 2: Gathering GitHub API data (Issues, PRs)...")
    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo(repo_full_name)
    
    # APIの since は「更新日」基準のため、作成日が古いものが混じる可能性がある
    issues = repo.get_issues(state='all', since=datetime.datetime(start_year, 1, 1))
    
    for i, issue in enumerate(issues):
        created_yr = issue.created_at.year
        yearly_stats[created_yr]["new_issues"] += 1
        
        if issue.closed_at:
            closed_yr = issue.closed_at.year
            yearly_stats[closed_yr]["closed_issues"] += 1
            # 作成からクローズまでの日数
            duration = (issue.closed_at - issue.created_at).days
            yearly_stats[closed_yr]["pr_durations"].append(duration)
            
        if i % 100 == 0: print(f"  Processed {i} items...", end="\r")

    # 4. 集計結果のフィルタリングと出力
    output_data = {
        "project": repo_full_name,
        "generated_at": datetime.datetime.now().isoformat(),
        "start_year_requested": start_year,
        "metrics": {}
    }

    print("\n\n" + "="*165)
    print(f"{'Year':<5} | {'Commits':<7} | {'Total':<5} | {'Active':<6} | {'CAF':<3} | {'Orgs':<4} | {'Elephant':<8} | {'NewIss':<7} | {'ClsIss':<7} | {'AvgDaysToCls':<12}")
    print("-" * 165)

    for yr in sorted(yearly_stats.keys()):
        # ここで引数で指定した年より古い「ゴミデータ」を完全に除外する
        if yr < start_year:
            continue
            
        s = yearly_stats[yr]
        
        # 貢献層分析 (N=10)
        counts = s["commit_counts"].values()
        active = [c for c in counts if c >= 10]
        
        # CAF (Bus Factor) 計算
        total_c = s["total_commits"]
        indiv_sorted = sorted(counts, reverse=True)
        caf, cum = 0, 0
        if total_c > 0:
            for c in indiv_sorted:
                cum += c; caf += 1
                if cum >= (total_c * 0.5): break
        
        # Elephant Factor 計算
        org_count = len(s["org_commit_counts"])
        org_sorted = sorted(s["org_commit_counts"].values(), reverse=True)
        total_org_c = sum(org_sorted)
        elephant, cum_o = 0, 0
        if total_org_c > 0:
            for oc in org_sorted:
                cum_o += oc; elephant += 1
                if cum_o >= (total_org_c * 0.5): break
        else:
            elephant = 1

        # 平均クローズ日数
        avg_close = sum(s["pr_durations"]) / len(s["pr_durations"]) if s["pr_durations"] else 0

        # コンソール表示
        print(f"{yr:<5} | {total_c:<7} | {len(counts):<5} | {len(active):<6} | {caf:<3} | {org_count:<4} | {elephant:<8} | "
              f"{s['new_issues']:<7} | {s['closed_issues']:<7} | {avg_close:<12.1f}")

        # JSONデータ蓄積
        output_data["metrics"][yr] = {
            "total_commits": total_c,
            "contrib_total": len(counts),
            "contrib_active_n10": len(active),
            "bus_factor_caf": caf,
            "org_count": org_count,
            "elephant_factor": elephant,
            "issues_new": s["new_issues"],
            "issues_closed": s["closed_issues"],
            "avg_days_to_close": round(avg_close, 2)
        }

    # 5. ファイル保存
    output_dir = "./output"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    safe_name = repo_full_name.replace('/','_')
    output_file = os.path.join(output_dir, f"{safe_name}_final_report.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

    print("-" * 165)
    print(f"Success! Final data saved to: {output_file}\n")

if __name__ == "__main__":
    main()