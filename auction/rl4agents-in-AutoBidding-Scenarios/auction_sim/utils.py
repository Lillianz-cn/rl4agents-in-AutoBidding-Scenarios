import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import PercentFormatter

class ResultVisualizer:
    def __init__(self, output_dir="results"):
        """初始化可视化工具"""
        os.makedirs(output_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = output_dir
        plt.switch_backend('Agg')  # 无GUI模式

    def save_visualizations(self, agents, warmup_rounds=0):
        """保存两种核心图表"""
        try:
            self._plot_cumulative_profit(agents, warmup_rounds)
            self._plot_roi_evolution(agents, warmup_rounds)
            print(f"核心图表已保存到 {os.path.abspath(self.output_dir)}/")
        except Exception as e:
            print(f"图表生成失败: {str(e)}")

    def _plot_cumulative_profit(self, agents, warmup_rounds):
        """绘制累计利润曲线"""
        plt.figure(figsize=(12, 6), dpi=120)
        
        for agent in agents:
            # 安全获取利润数据
            profits = np.array([r.get('profit', 0) for r in getattr(agent, 'history', []) 
                              if isinstance(r, dict)])
            cumulative = np.cumsum(profits)
            
            # 分阶段绘制
            if warmup_rounds > 0:
                plt.plot(range(warmup_rounds), cumulative[:warmup_rounds], 
                        ':', color='gray', alpha=0.5)
                plt.plot(range(warmup_rounds, len(cumulative)), cumulative[warmup_rounds:],
                        label=agent.id, linewidth=1.5)
            else:
                plt.plot(cumulative, label=agent.id, linewidth=1.5)
        
        if warmup_rounds > 0:
            plt.axvline(warmup_rounds, color='r', linestyle='--', alpha=0.3, label='Warmup End')
        
        plt.title("Cumulative Profit by Agent")
        plt.xlabel("Auction Round")
        plt.ylabel("Profit")
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        path = f"{self.output_dir}/profit_{self.timestamp}.png"
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        print(f"利润曲线已保存: {path}")

    def _plot_roi_evolution(self, agents, warmup_rounds):
        """绘制ROI演化曲线"""
        plt.figure(figsize=(12, 6), dpi=120)
        
        for agent in agents:
            roi = []
            cum_cost = 0
            cum_profit = 0
            
            # 安全计算ROI
            for r in getattr(agent, 'history', []):
                if isinstance(r, dict):
                    cum_cost += r.get('cost', 0)
                    cum_profit += r.get('profit', 0)
                    roi.append((cum_profit / cum_cost * 100) if cum_cost > 0 else 0)
            
            roi = np.array(roi)
            
            if warmup_rounds > 0:
                plt.plot(range(warmup_rounds), roi[:warmup_rounds], 
                        ':', color='gray', alpha=0.5)
                plt.plot(range(warmup_rounds, len(roi)), roi[warmup_rounds:],
                        label=agent.id, linewidth=1.5)
            else:
                plt.plot(roi, label=agent.id, linewidth=1.5)
        
        if warmup_rounds > 0:
            plt.axvline(warmup_rounds, color='r', linestyle='--', alpha=0.3, label='Warmup End')
        
        plt.title("ROI Evolution by Agent")
        plt.xlabel("Auction Round")
        plt.ylabel("ROI (%)")
        plt.gca().yaxis.set_major_formatter(PercentFormatter())
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        path = f"{self.output_dir}/roi_{self.timestamp}.png"
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        print(f"ROI曲线已保存: {path}")
