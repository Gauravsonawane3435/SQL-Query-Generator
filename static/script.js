document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt');
    const dialectSelect = document.getElementById('dialect');
    const generateBtn = document.getElementById('generate-btn');
    const clearBtn = document.getElementById('clear-btn');
    const outputContainer = document.getElementById('output-container');
    const outputSql = document.getElementById('output-sql');
    const explanationText = document.getElementById('explanation-text');
    const copyBtn = document.getElementById('copy-btn');

    // Handle Generation
    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();
        const dialect = dialectSelect.value;

        if (!prompt) {
            alert('Please enter a description for your query.');
            return;
        }

        // UI Loading State
        generateBtn.classList.add('loading');
        generateBtn.disabled = true;

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt, dialect }),
            });

            if (!response.ok) {
                throw new Error('Failed to generate SQL');
            }

            const data = await response.json();

            // Display Output
            outputSql.textContent = data.sql;
            explanationText.textContent = data.explanation;
            outputContainer.classList.remove('hidden');
            
            // Re-highlight code
            Prism.highlightElement(outputSql);

            // Scroll to output
            outputContainer.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating the SQL query. Please try again.');
        } finally {
            generateBtn.classList.remove('loading');
            generateBtn.disabled = false;
        }
    });

    // Clear Logic
    clearBtn.addEventListener('click', () => {
        promptInput.value = '';
        outputContainer.classList.add('hidden');
        promptInput.focus();
    });

    // Copy to Clipboard
    copyBtn.addEventListener('click', () => {
        const sql = outputSql.textContent;
        navigator.clipboard.writeText(sql).then(() => {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span>Copied!</span>
            `;
            copyBtn.style.color = '#10b981';
            copyBtn.style.borderColor = '#10b981';

            setTimeout(() => {
                copyBtn.innerHTML = originalText;
                copyBtn.style.color = '';
                copyBtn.style.borderColor = '';
            }, 2000);
        });
    });

    // Ctrl+Enter to submit
    promptInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            generateBtn.click();
        }
    });
});
