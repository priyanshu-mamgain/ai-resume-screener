// Give it a case-file number for flavor
document.getElementById('fileTag').innerText =
  'FILE NO. ' + String(Math.floor(Math.random() * 9000) + 1000);

const dropZone = document.getElementById('dropZone');
const resumeFile = document.getElementById('resumeFile');
const fileLabel = document.getElementById('fileLabel');
const resumeText = document.getElementById('resumeText');

dropZone.addEventListener('click', () => resumeFile.click());

resumeFile.addEventListener('change', () => {
  if (resumeFile.files.length > 0) {
    fileLabel.innerText = "📎 " + resumeFile.files[0].name;
    resumeText.value = "";
  }
});

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  if (e.dataTransfer.files.length > 0) {
    resumeFile.files = e.dataTransfer.files;
    fileLabel.innerText = "📎 " + e.dataTransfer.files[0].name;
    resumeText.value = "";
  }
});

async function screenResume() {
  const jd = document.getElementById('jd').value.trim();
  const pastedText = resumeText.value.trim();
  const file = resumeFile.files[0];
  const errorBox = document.getElementById('errorBox');
  const resultArea = document.getElementById('result');
  const btn = document.getElementById('checkBtn');
  const btnText = document.getElementById('btnText');
  const btnLoader = document.getElementById('btnLoader');

  errorBox.style.display = 'none';
  resultArea.style.display = 'none';

  if (!jd || (!pastedText && !file)) {
    showError("Add a resume (file or text) and a job description first.");
    return;
  }

  btn.disabled = true;
  btnText.innerText = "Reviewing...";
  btnLoader.style.display = 'inline-block';

  try {
    let response;

    if (file) {
      const formData = new FormData();
      formData.append('resume_file', file);
      formData.append('job_description', jd);

      response = await fetch('/screen', {
        method: 'POST',
        body: formData
      });
    } else {
      response = await fetch('/screen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_text: pastedText, job_description: jd })
      });
    }

    const data = await response.json();

    if (!response.ok || data.error) {
      showError(data.error || "Something went wrong. Try again.");
      return;
    }

    displayResult(data.score, data.missing_keywords);

  } catch (err) {
    showError("Could not reach the server.");
  } finally {
    btn.disabled = false;
    btnText.innerText = "Stamp It";
    btnLoader.style.display = 'none';
  }
}

function displayResult(score, keywords) {
  const resultArea = document.getElementById('result');
  const scoreValue = document.getElementById('scoreValue');
  const verdictText = document.getElementById('verdictText');
  const stamp = document.getElementById('stamp');
  const keywordsValue = document.getElementById('keywordsValue');

  resultArea.style.display = 'block';
  scoreValue.innerText = score + '%';

  let verdict = 'WEAK MATCH';
  let color = 'var(--rust)';
  if (score >= 70) { verdict = 'STRONG MATCH'; color = 'var(--gold-dark)'; }
  else if (score >= 40) { verdict = 'FAIR MATCH'; color = 'var(--amber-mid)'; }

  verdictText.innerText = verdict;
  stamp.style.borderColor = color;
  scoreValue.style.color = color;
  verdictText.style.color = color;

  // Restart the stamp animation
  stamp.style.animation = 'none';
  stamp.offsetHeight; // trigger reflow
  stamp.style.animation = 'stamp-hit 0.35s ease-out';

  keywordsValue.innerHTML = '';
  if (keywords.length === 0) {
    keywordsValue.innerHTML = '<span>Nothing major missing.</span>';
  } else {
    keywords.forEach(word => {
      const span = document.createElement('span');
      span.innerText = word;
      keywordsValue.appendChild(span);
    });
  }

  resultArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(msg) {
  const errorBox = document.getElementById('errorBox');
  errorBox.innerText = msg;
  errorBox.style.display = 'block';
}