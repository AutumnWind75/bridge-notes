---
layout: ../../layouts/Layout.astro
title: 桥牌叫牌学习大纲
---

<div class="header">
  <h1>🃏 桥牌叫牌学习大纲</h1>
  <p>从零开始，循序渐进掌握核心叫牌逻辑。</p>
</div>

<div class="course-grid">

  <a href="./chapters/01-normal-opening" class="course-card">
    <div class="card-icon">♠️</div>
    <div class="card-content">
      <h2>第一章：正常开叫与阻击开叫</h2>
      <p>学习评估手牌，掌握 1 阶花色、无将、 2♣ 以及高阶阻击的开叫条件。</p>
    </div>
  </a>

  <a href="./chapters/02-first-response" class="course-card">
    <div class="card-icon">♥️</div>
    <div class="card-content">
      <h2>第二章：一阶花色应叫</h2>
      <p>搭档开叫 1 阶花色后，如何通过一盖一或加叫传达牌型。</p>
    </div>
  </a>

  <a href="./chapters/03-nt-response" class="course-card">
    <div class="card-icon">♦️</div>
    <div class="card-content">
      <h2>第三章：无将应叫</h2>
      <p>当搭档开叫后，如何正确使用 1NT 和 2NT 进行建设性应叫。</p>
    </div>
  </a>

  <a href="./chapters/04-strong-response" class="course-card">
    <div class="card-icon">♣️</div>
    <div class="card-content">
      <h2>第四章：2♣ 强牌应叫</h2>
      <p>面对搭档的 2♣ 强开叫，如何展开满贯问叫与探索。</p>
    </div>
  </a>

  <a href="./chapters/05-preemptive-opening" class="course-card">
    <div class="card-icon">🚧</div>
    <div class="card-content">
      <h2>第五章：阻击叫应叫</h2>
      <p>当搭档进行弱二或三阶阻击时，作为应叫方如何判断进局或牺牲叫。</p>
    </div>
  </a>

  <a href="./chapters/06-competitive-bidding" class="course-card">
    <div class="card-icon">⚔️</div>
    <div class="card-content">
      <h2>第六章：竞争叫</h2>
      <p>当对手参与叫牌时，如何通过加倍、争叫等方式夺回主动权。</p>
    </div>
  </a>

</div>

<style>
  .header {
    text-align: center;
    margin-bottom: 3rem;
    margin-top: 2rem;
  }
  .header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }
  .header p {
    color: #666;
    font-size: 1.1rem;
  }

  .course-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
    max-width: 800px;
    margin: 0 auto;
    padding: 0 1rem;
  }
  @media (min-width: 600px) {
    .course-grid {
      grid-template-columns: 1fr 1fr;
    }
  }

  .course-card {
    display: flex;
    align-items: flex-start;
    padding: 1.5rem;
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 12px;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  }
  .course-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.08);
    border-color: #8b5cf6;
  }

  .card-icon {
    font-size: 2rem;
    margin-right: 1rem;
  }
  .card-content h2 {
    font-size: 1.2rem;
    margin: 0 0 0.5rem 0;
    color: #222;
  }
  .card-content p {
    font-size: 0.9rem;
    margin: 0;
    color: #555;
    line-height: 1.4;
  }
</style>
