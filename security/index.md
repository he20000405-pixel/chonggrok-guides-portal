---
layout: default
title: "ChongGrok 账号资料与会员服务安全说明"
seo_title: "AI 会员服务安全说明"
description: "了解 ChongGrok 不需要密码的服务边界、ChatGPT session 与 User ID 的敏感性、最少资料原则和订单安全检查。"
permalink: /security/
current: security
---

<section class="page-hero">
  <div class="shell">
    <p class="eyebrow">Security</p>
    <h1>不索要密码，只提交本次服务需要的资料</h1>
    <p>ChongGrok 不要求提供账号密码、验证码或恢复码。部分产品需要 session 或 User ID 来匹配账号，这些信息虽然不是密码，仍应按敏感资料谨慎处理。</p>
  </div>
</section>

<section class="section">
  <div class="shell content-layout">
    <article class="prose">
      <h2 id="never">这些资料不要提交</h2>
      <ul class="check-list">
        <li>账号密码，以及任何能够直接登录账号的信息。</li>
        <li>短信、邮箱或身份验证器生成的验证码。</li>
        <li>恢复码、备用代码和能够重置账号的恢复资料。</li>
        <li>与本次订单无关的银行卡完整信息、证件或私人文件。</li>
      </ul>

      <h2 id="minimum">不同产品的最少资料</h2>
      <div class="table-scroll" role="region" aria-label="各产品最少资料说明" tabindex="0">
      <table>
        <thead><tr><th>产品</th><th>可能使用的资料</th><th>需要注意什么</th></tr></thead>
        <tbody>
          <tr><td>ChatGPT</td><td>Plus 自助流程使用 session 类凭证</td><td>它代表当前登录会话，不能公开；完成后建议重新登录刷新</td></tr>
          <tr><td>Grok</td><td>Grok User ID</td><td>它用于匹配目标账号，不是密码；仍应只在确认的订单流程中提交</td></tr>
          <tr><td>Claude</td><td>客服说明的 User ID</td><td>它是 ChongGrok 履约标识，不是 Anthropic 官方订阅要求</td></tr>
          <tr><td>Gemini</td><td>取决于具体账号类型和服务方案</td><td>提交前由产品页或客服说明，不固定宣称统一凭证</td></tr>
        </tbody>
      </table>
      </div>

      <h2 id="before">提交前检查四件事</h2>
      <ol>
        <li>确认浏览器中的域名、产品名称和订单信息一致。</li>
        <li>确认当前登录的正是需要处理的目标账号。</li>
        <li>删除截图中与本次订单无关的个人信息。</li>
        <li>任何渠道要求密码、验证码或恢复码时，立即停止提交。</li>
      </ol>

      <h2 id="after">完成后的安全检查</h2>
      <ol>
        <li>回产品官方页面检查会员状态，不只依据付款截图判断结果。</li>
        <li>保存订单号、卡密和处理结果，售后沟通时只提供脱敏证据。</li>
        <li>ChatGPT session 流程完成后，建议退出并重新登录。</li>
        <li>已有扣款或订单仍在处理时，不要重复购买。</li>
      </ol>

      <div class="notice">
        <strong>风险边界：</strong>不需要密码不等于绝对安全。账号状态、支付渠道、地区规则和产品方风控都可能影响结果。ChongGrok 不承诺所有账号均可处理，也不作固定完成时间或零风险保证。
      </div>

      <div class="button-row">
        <a class="button" href="https://he20000405-pixel.github.io/resources/ai-membership-safety-checklist/" rel="noopener">打开 AI 会员安全清单</a>
        <a class="button" href="/how-it-works/">查看服务流程</a>
      </div>
    </article>
    <nav class="side-nav" aria-label="本页目录">
      <strong>本页目录</strong>
      <a href="#never">禁止提交</a>
      <a href="#minimum">最少资料</a>
      <a href="#before">提交前</a>
      <a href="#after">完成后</a>
    </nav>
  </div>
</section>
