document.addEventListener('DOMContentLoaded', function () {
  const tableBody = document.querySelector('#pantoneTable tbody');
  const searchInput = document.getElementById('search');
  const sortByNameButton = document.querySelectorAll('button')[0];
  const sortByCodeButton = document.querySelectorAll('button')[1];

  async function loadPantoneData() {
    try {
      const response = await fetch('pantone_colors.txt');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const text = await response.text();
      return text.split('\n').filter(line => line.trim() !== '');
    } catch (error) {
      console.error('Error loading file:', error);
      return [];
    }
  }

  function renderTable(data) {
    tableBody.innerHTML = '';
    data.forEach(item => {
      const [name, code] = item.split(' - ');
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${name}</td>
        <td>${code}</td>
        <td><button onclick="copyToClipboard('${code}')">Copy</button></td>
      `;
      tableBody.appendChild(row);
    });
  }

  window.copyToClipboard = function (text) {
    navigator.clipboard.writeText(text).then(() => {
      alert('Code copied to clipboard!');
    });
  };

  async function updateTable() {
    const data = await loadPantoneData();
    filterTable(data);
  }

  function filterTable(data) {
    const searchTerm = searchInput.value.toLowerCase();
    const filteredData = data.filter(item => item.toLowerCase().includes(searchTerm));
    renderTable(filteredData);
  }

  function sortTable(data, byCode = false) {
    const sortedData = [...data].sort((a, b) => {
      const [nameA, codeA] = a.split(' - ');
      const [nameB, codeB] = b.split(' - ');

      return byCode ? codeA.localeCompare(codeB) : nameA.localeCompare(nameB);
    });
    renderTable(sortedData);
  }

  searchInput.addEventListener('input', async () => {
    const data = await loadPantoneData();
    filterTable(data);
  });

  sortByNameButton.addEventListener('click', async () => {
    const data = await loadPantoneData();
    sortTable(data);
  });

  sortByCodeButton.addEventListener('click', async () => {
    const data = await loadPantoneData();
    sortTable(data, true);
  });

  updateTable();
});
