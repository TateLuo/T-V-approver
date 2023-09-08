import sqlite3
import numpy as np


class ApprovalLevelData:
    def get_approval_level_data(self, username):
        try:
            # Connect to database
            conn = sqlite3.connect('database.db')

            # Execute SQL query
            cursor = conn.cursor()
            cursor.execute("SELECT status_approve FROM approval WHERE approver=?", (username,))

            # Count values
            pending_count = 0
            approve_count = 0
            reject_count = 0

            for row in cursor.fetchall():
                if row[0] == "pending":
                    pending_count += 1
                elif row[0] == "同意":
                    approve_count += 1
                elif row[0] == "不同意":
                    reject_count += 1

            # Close connection
            conn.close()
            sum_count = pending_count+pending_count+pending_count
            if sum_count != 0:
                approved_rate = (approve_count/sum_count)*100
                # Return counts as dictionary
                print(pending_count)
                return {"pending": pending_count, "approve": approve_count, "reject": reject_count, "approved_rate":str(approved_rate)+"%"}
            else:
                return {"pending": pending_count, "approve": approve_count, "reject": reject_count, "approved_rate":"还没审批过呢"}
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
            
    #根据相关数据计算严厉等级
    def calculate_score(self, pending_score, approved_score, reject_score):
        sumScore = sum([pending_score, approved_score, reject_score]);
        
        if sumScore == 0:
            return '审批小白'
        else:
            if approved_score/sumScore == 0:
                return "无情的刀"
            elif approved_score/sumScore in np.arange(0,0.1,0.001):
                return "无情的刀"
            elif approved_score/sumScore in np.arange(0.1,0.2,0.001):
                return "秉公无私"
            elif approved_score/sumScore in np.arange(0.2,0.3,0.001):
                return "冷酷无情"
            elif approved_score/sumScore in np.arange(0.3,0.4,0.001):
                return "刻薄无情"
            elif approved_score/sumScore in np.arange(0.4,0.5,0.001):
                return "铁面无私"
            elif approved_score/sumScore in np.arange(0.5,0.6,0.001):
                return "一丝不苟"
            elif approved_score/sumScore in np.arange(0.6,0.7,0.001):
                return "稳重严格"
            elif approved_score/sumScore in np.arange(0.7,0.8,0.001):
                return "细心严谨"
            elif approved_score/sumScore in np.arange(0.8,0.9,0.001):
                return "温和审慎"
            elif approved_score/sumScore in np.arange(0.9,1,0.001):
                return "宰相肚里能撑船"
            else:
                return "审批小白"
