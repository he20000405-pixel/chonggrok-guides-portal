---
layout: default
title: "ChongGrok 账号资料与会员服务安全说明"
seo_title: "AI 会员服务安全说明"
description: "区分 ChatGPT session、X 联合会员 Grok SSO 与旧版 Grok User ID，了解登录凭据风险、资料边界和订单安全检查。"
permalink: /security/
current: security
last_modified_at: 2026-10-28
---

<section class="page-hero">
  <div class="shell">
    <p class="eyebrow">Security</p>
    <h1>不索要密码，只提交本次服务需要的资料</h1>
    <p>ChongGrok 不要求账号密码、验证码或恢复码，但部分流程仍需登录凭据。ChatGPT session 与 Grok SSO 可以代表登录会话；User ID 只是账号标识。三者不能互换，也不能因为不填写密码就认定没有账号访问风险。</p>
  </div>
</section>

<section class="section">
  <div class="shell content-layout">
    <article class="prose">
      <h2 id="never">这些资料不要提交</h2>
      <ul class="check-list">
        <li>账号密码，以及与本次订单无关的 Cookie、完整会话或登录资料。</li>
        <li>短信、邮箱或身份验证器生成的验证码。</li>
        <li>恢复码、备用代码和能够重置账号的恢复资料。</li>
        <li>与本次订单无关的银行卡完整信息、证件或私人文件。</li>
      </ul>

      <h2 id="minimum">不同产品的最少资料</h2>
      <div class="table-scroll" role="region" aria-label="各产品最少资料说明" tabindex="0">
      <table>
        <thead><tr><th>产品</th><th>可能使用的资料</th><th>需要注意什么</th></tr></thead>
        <tbody>
          <tr><td>ChatGPT</td><td>Plus 自助流程使用 session 类凭证</td><td>它代表登录会话；先理解用途，只在确认的兑换入口按字段提交，不公开传播</td></tr>
          <tr><td>X 联合会员</td><td>Grok SSO，兑换入口 /verify-x</td><td>SSO 是敏感登录凭据，不是 User ID；不应把临时凭据理解为无风险或自动失效保证</td></tr>
          <tr><td>旧版 SuperGrok</td><td>Grok User ID，兑换入口 /verify-grok</td><td>它用于定位账号；只提交要求的 userId，不提交完整 session、Cookie 或 SSO</td></tr>
          <tr><td>Claude Pro</td><td>人工开通前由客服说明必要账号标识</td><td>不发送密码、验证码、完整会话或私密项目；如需身份验证，只由本人在官方入口提交</td></tr>
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
        <li>使用过 session 或 SSO 后，按产品官方安全设置检查登录设备与会话，结束不再需要的会话。</li>
        <li>已有扣款或订单仍在处理时，不要重复购买。</li>
      </ol>

      <div class="notice">
        <strong>风险边界：</strong>不需要密码不等于无需敏感凭据。账号状态、支付渠道、地区规则和产品方风控都可能影响结果。ChongGrok 不保证所有账号可办理、固定完成时间或零风险。Claude Pro 成功开通后的官方风控封号不提供质保；身份验证不由本站代办。
      </div>

      <p><a href="https://x.ai/pricing" rel="noopener">xAI 定价页</a>说明未授权第三方销售，其他来源的账号可能被暂停或终止。选择 Grok 服务前，应同时了解这项政策与凭据用途；如不接受这些条件，请停止第三方办理并查看官方购买渠道。</p>

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
