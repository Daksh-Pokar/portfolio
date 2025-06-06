const multer = require('multer');
const upload = multer({ dest: 'uploads/' });

app.use('/uploads', express.static('uploads'));

app.post('/api/projects', upload.single('image'), (req, res) => {
  const { projectName: name, projectDescription: description } = req.body;
  const image = req.file ? `/uploads/${req.file.filename}` : null;

  const newProject = { name, description, image };

  fs.readFile(PROJECTS_FILE, 'utf8', (err, data) => {
    const projects = data ? JSON.parse(data) : [];
    projects.push(newProject);

    fs.writeFile(PROJECTS_FILE, JSON.stringify(projects, null, 2), (err) => {
      if (err) {
        res.status(500).send('Error saving project');
      } else {
        res.send('Project saved!');
      }
    });
  });
});
