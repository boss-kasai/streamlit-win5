from itertools import product

import pandas as pd
import streamlit as st

# Streamlitアプリの設定
st.title("WIN5 人気順位合計値パターン計算アプリ")

# 入力フォーム
st.subheader("基本設定")
col1, col2 = st.columns(2)  # 2列に分割
with col1:
    total_sum = st.number_input(
        "合計値を入力してください (例: 14)",
        min_value=5,
        max_value=100,
        value=14,
        step=1,
    )
with col2:
    max_rank = st.number_input(
        "人気順位の最大値を入力してください (例: 18)",
        min_value=2,
        max_value=50,
        value=18,
        step=1,
    )

# 各レースの条件入力
st.subheader("レースごとの条件設定（任意）")
columns = st.columns(5)  # 5列に分割
race_conditions = []
for i, col in enumerate(columns, start=1):
    with col:
        condition = st.number_input(
            f"レース{i}の人気順位",
            min_value=0,
            max_value=max_rank,
            value=0,
            step=1,
            key=f"race_{i}",
        )
        race_conditions.append(
            condition if condition != 0 else None
        )  # 0は指定なしとして扱う

# 計算ボタン
if st.button("計算"):
    try:
        # ローディングスピナーの表示
        with st.spinner("計算中です。しばらくお待ちください..."):
            # 合計値から未指定レースの順位の合計範囲を計算
            specified_sum = sum(cond for cond in race_conditions if cond is not None)
            remaining_sum = total_sum - specified_sum
            remaining_races = sum(1 for cond in race_conditions if cond is None)

            # 各未指定レースで可能な範囲を計算
            st.write("未指定のレースの値として入り得る範囲:")
            min_value = max(1, remaining_sum - (max_rank * (remaining_races - 1)))
            max_value = min(max_rank, remaining_sum - (1 * (remaining_races - 1)))
            st.write(f"{min_value} ～ {max_value}")

            # 全てのレース（5つ）の人気順位の組み合わせを生成
            possible_combinations = list(product(range(1, max_rank + 1), repeat=5))

            # 合計値に合致するパターンをフィルタリング
            matching_patterns = [
                comb
                for comb in possible_combinations
                if sum(comb) == total_sum
                and all(
                    race_conditions[i] is None or comb[i] == race_conditions[i]
                    for i in range(5)
                )
            ]

        # スピナーが消え、結果が表示される
        st.success("計算が完了しました！")

        # 結果の表示
        st.write(
            f"合計値 {total_sum} を満たすパターン数: {len(matching_patterns)} 通り"
        )

        # 詳細結果の表示
        if len(matching_patterns) > 0:
            if len(matching_patterns) <= 100:
                # 100件以下の場合は表形式で表示
                st.write("パターン一覧（表形式）:")
                df = pd.DataFrame(
                    matching_patterns,
                    columns=["レース1", "レース2", "レース3", "レース4", "レース5"],
                )

                # スタイルを適用する関数
                def highlight_fixed_columns(row):
                    style = []
                    for i, condition in enumerate(race_conditions):
                        if condition is not None:
                            style.append("background-color: lightgrey")
                        else:
                            style.append("")
                    return style

                # スタイル付きデータフレームを表示
                styled_df = df.style.apply(highlight_fixed_columns, axis=1)
                st.dataframe(styled_df)
            else:
                # 100件を超える場合はメッセージのみ表示
                st.write("パターンが100通りを超えています。条件を変更してください。")
        else:
            st.write("指定された条件を満たすパターンは見つかりませんでした。")

    except Exception as e:
        # エラー時の処理
        st.error(f"計算中にエラーが発生しました: {e}")
