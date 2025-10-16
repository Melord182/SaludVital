from django.db import migrations, models
import django.db.models.deletion

def forwards(apps, schema_editor):
    Medicamento = apps.get_model('gestion_clinica', 'Medicamento')
    Laboratorio = apps.get_model('gestion_clinica', 'Laboratorio')

    # 1) Crear Laboratorios a partir de los textos existentes en Medicamento.laboratorio_old
    #    (campo original de texto). Si tu campo antiguo se llamaba también 'laboratorio',
    #    aquí asumimos que en este paso aún existe como CharField y el nuevo se llama laboratorio_fk.
    seen = {}
    for med in Medicamento.objects.all():
        nombre_txt = getattr(med, 'laboratorio', None)
        if not nombre_txt:
            continue
        nombre_norm = str(nombre_txt).strip()
        if not nombre_norm:
            continue
        if nombre_norm not in seen:
            lab = Laboratorio.objects.create(nombre=nombre_norm, pais='Chile')  # ajusta país si corresponde
            seen[nombre_norm] = lab.id
        # asigna al campo temporal FK
        setattr(med, 'laboratorio_fk_id', seen[nombre_norm])
        med.save(update_fields=['laboratorio_fk'])

def backwards(apps, schema_editor):
    # Nada seguro que revertir automáticamente (de FK a texto),
    # podrías copiar el nombre de vuelta si añadieras un campo texto temporal.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('gestion_clinica', '0001_initial'),
    ]

    operations = [
        # 0) Asegúrate de que el modelo Laboratorio exista antes de mapear
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('pais', models.CharField(max_length=100)),
                ('direccion', models.CharField(blank=True, max_length=200)),
                ('telefono', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Laboratorio',
                'verbose_name_plural': 'Laboratorios',
                'ordering': ['nombre'],
            },
        ),

        # 1) Agregar un campo FK temporal y nullable
        migrations.AddField(
            model_name='medicamento',
            name='laboratorio_fk',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='medicamentos', to='gestion_clinica.laboratorio'),
        ),

        # 2) Poblar laboratorio_fk desde el texto existente
        migrations.RunPython(forwards, backwards),

        # 3) Eliminar el campo de texto antiguo
        migrations.RemoveField(
            model_name='medicamento',
            name='laboratorio',
        ),

        # 4) Renombrar laboratorio_fk -> laboratorio
        migrations.RenameField(
            model_name='medicamento',
            old_name='laboratorio_fk',
            new_name='laboratorio',
        ),

        # 5) Hacer obligatorio (null=False)
        migrations.AlterField(
            model_name='medicamento',
            name='laboratorio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medicamentos', to='gestion_clinica.laboratorio'),
        ),
    ]
