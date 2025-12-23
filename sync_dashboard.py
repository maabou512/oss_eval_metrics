import os
import re
import json

def sync():
    html_path = "index.html"
    output_dir = "./output"
    
    if not os.path.exists(output_dir):
        print(f"Error: {output_dir} folder not found.")
        return

    # 1. outputフォルダ内の有効なレポートをスキャン
    project_files = []
    # ファイル名の昇順でソートして読み込み順を安定させる
    for filename in sorted(os.listdir(output_dir)):
        if filename.endswith("_final_report.json"):
            # IDと表示名を生成
            p_id = filename.replace("_final_report.json", "")
            # 名前はファイル名の先頭部分などを利用（例: postgres_postgres -> postgres）
            display_name = p_id.split('_')[0].capitalize() 
            
            project_files.append({
                "id": p_id,
                "name": display_name,
                "file": f"output/{filename}"
            })
    
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found in current directory.")
        return

    # 2. index.html の projectFiles 配列を置換
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # JavaScriptの配列部分を正規表現でキャッチして置換
    json_list_str = json.dumps(project_files, indent=8, ensure_ascii=False)
    new_content = re.sub(
        r'const projectFiles = \[.*?\];',
        f'const projectFiles = {json_list_str};',
        content,
        flags=re.DOTALL
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Dashboard updated with {len(project_files)} projects from '{output_dir}'.")

if __name__ == "__main__":
    sync()