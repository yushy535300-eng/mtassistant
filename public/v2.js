(() => {
  const form = document.querySelector('#v2-support-form');
  if (!form) return;
  const summary = document.querySelector('#v2-summary');
  const copy = document.querySelector('#v2-copy');
  const status = document.querySelector('#v2-copy-status');
  form.addEventListener('submit', e => {
    e.preventDefault();
    summary.value = `御策百家客服問題\n使用系統：${document.querySelector('#v2-system').value}\n問題類型：${document.querySelector('#v2-topic').value}\n問題描述：${document.querySelector('#v2-issue').value.trim() || '待補充'}\n裝置／瀏覽器：\n發生時間：`;
    copy.disabled = false; status.textContent = '摘要已產生，請核對內容。';
  });
  copy.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(summary.value); status.textContent = '已複製摘要。'; }
    catch { summary.focus(); summary.select(); status.textContent = '請手動複製已選取的摘要。'; }
  });
})();
