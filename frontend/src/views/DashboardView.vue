<template>
  <DashboardLayout>
    <div class="header">
      <h1>Vite app</h1>
    </div>

    <div class="filters">
      <input placeholder="ФИО" />
      <input placeholder="Дата рождения" />
      <input placeholder="Статус" />
    </div>

    <table>
      <thead>
        <tr>
          <th>ФИО</th>
          <th>Дата рождения</th>
          <th>Статус</th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td>Иванов Василий Александрович</td>
          <td>01.12.1905</td>
          <td>Опубликовано</td>
        </tr>
      </tbody>
    </table>
  </DashboardLayout>
</template>

<style scoped>
.filters {
  display: flex;
  gap: 12px;
  margin: 24px 0;
}

.filters input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

th,
td {
  border-bottom: 1px solid #eee;
  padding: 16px;
  text-align: left;
}
</style>