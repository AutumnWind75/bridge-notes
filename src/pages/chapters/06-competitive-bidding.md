---
layout: ../../layouts/Layout.astro
title: 第六章：竞争叫
---

# 第六章：竞争叫

## 敌方开叫 1Y 后的应叫策略

<div class="quote-box">
  <p>为了便于描述，我们设定：敌方开叫了 <strong>1Y</strong>。<strong>Z</strong> 代表比 Y 级别更高的未叫花色，<strong>X</strong> 代表比 Y 级别更低的未叫花色。</p>
</div>

<div class="j2nt-table-wrapper">
<table class="j2nt-table">
<thead>
<tr>
<th>阶数</th>
<th>NT</th>
<th>Z（较高级未叫套）</th>
<th style="color: #e11d48;">Y（敌方开叫）</th>
<th>X（较低级未叫套）</th>
</tr>
</thead>
<tbody>
<tr>
<td class="call-col"><strong>1 阶</strong></td>
<td>第 2 家：15-18 点，均型<br>第 4 家：12-15 点，均型<br>后续应叫同开1NT</td>
<td>5+ 套，8-16 点</td>
<td style="color: #94a3b8;">——</td>
<td style="color: #94a3b8;">——</td>
</tr>
<tr>
<td class="call-col"><strong>2 阶</strong></td>
<td>第 2 家：<strong>最低级别的 2 个未叫套</strong><br>第 4 家：19-20 点，后 <strong>3♣ Stayman</strong></td>
<td>阻击叫</td>
<td><strong>迈克尔斯扣叫: </strong><br>若Y为低花则至少5-5高花，8+点，点集中在长套上<br>若Y为高花则5-5另一高花和任一低花，10+点，点集中在长套上</td>
<td>5+ 套，11-16 点</td>
</tr>
<tr>
<td class="call-col"><strong>3+ 阶</strong></td>
<td style="color: #94a3b8;">——</td>
<td>阻击叫</td>
<td><strong>有一低花坚固套，或是高花套不适合加倍的畸形牌</strong></td>
<td>阻击叫</td>
</tr>
</tbody>
</table>
</div>

---
<div class="chapter-nav">
  <a href="/chapters/05-preemptive-opening" class="nav-btn prev">← 上一章：应叫阻击叫</a>
  <a href="/chapters" class="nav-btn next">返回目录 →</a>
</div>

<style>
  /* 引用框样式 */
  .quote-box {
    border-left: 3px solid #cbd5e1;
    padding: 0.8rem 1rem;
    margin: 1.5rem 0;
    color: #64748b;
    background: #f8fafc;
    border-radius: 0 4px 4px 0;
    font-style: italic;
  }
  .quote-box p { margin: 0 0 0.5rem 0; line-height: 1.6; }
  .quote-box p:last-child { margin-bottom: 0; }

  /* 花色颜色 */
  .suit.red { color: #e11d48; font-size: 1.15em; line-height: 1; }
  .suit.black { color: #0f172a; font-size: 1.15em; line-height: 1; }

  /* 表格样式（和前面章节完全统一） */
  .j2nt-table-wrapper {
    margin-top: 1.5rem;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  .j2nt-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-size: 0.95rem;
    min-width: 600px;
  }
  .j2nt-table th {
    background: #f8fafc;
    padding: 12px 16px;
    color: #475569;
    font-weight: 600;
    border-bottom: 1px solid #e2e8f0;
    white-space: nowrap;
  }
  .j2nt-table td {
    padding: 12px 16px;
    border-bottom: 1px solid #f1f5f9;
    color: #334155;
    line-height: 1.5;
  }
  .j2nt-table tr:last-child td { border-bottom: none; }
  .j2nt-table tr:hover td { background: #f8fafc; }
  .call-col { width: 15%; white-space: nowrap; }

  /* 底部导航按钮 */
  .chapter-nav {
    display: flex;
    justify-content: space-between;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e2e8f0;
  }
  .nav-btn {
    display: inline-block;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.2s ease;
  }
  .nav-btn.prev { color: #64748b; background: #f8fafc; border: 1px solid #e2e8f0; }
  .nav-btn.prev:hover { background: #f1f5f9; color: #334155; }
  .nav-btn.next { color: white; background: #8b5cf6; border: 1px solid #8b5cf6; }
  .nav-btn.next:hover { background: #7c3aed; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); }
</style>