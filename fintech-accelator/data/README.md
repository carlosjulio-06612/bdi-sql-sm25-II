# Fintech Accelerator - Datos SQL

Este directorio contiene los datos SQL necesarios para ejecutar el proyecto Fintech Accelerator.

## Descarga de Datos

1. Descarga el archivo de datos desde el siguiente enlace:  
   [https://drive.google.com/file/d/1Amh4MIrRgattEr9RJ-gbiZnIf-nfYFg8/view?usp=sharing](https://drive.google.com/file/d/1Amh4MIrRgattEr9RJ-gbiZnIf-nfYFg8/view?usp=sharing)

2. Coloca el archivo ZIP descargado en la siguiente ruta:  
   `content/fintech-accelator/data/sql`

3. Descomprime el archivo ZIP en esta misma ubicación.

## Organización de Archivos

Después de descomprimir, deberás mover los archivos de la carpeta `SQL-Data/Bulk-Load` a la carpeta `sql/Bulk-Load`.

La estructura final de directorios debe verse así:

```
content/fintech-accelator/data/
└── sql/
    ├── Bulk-Load/
    │   ├── 04-FINTECH-CLIENTS_bulk_batches.sql
    │   ├── 05-FINTECH-ISSUERS_bulk_batches.sql
    │   ├── 06-FINTECH-FRANCHISES_bulk_batches.sql
    │   ├── 07-FINTECH-MERCHANT_LOCATIONS_bulk_batches.sql
    │   ├── 08-FINTECH-CREDIT_CARDS_bulk_batches.sql
    │   └── 09-FINTECH-TRANSACTIONS_bulk_batches.sql
    ├── FK-Values/
    │   ├── FK-FINTECH-COUNTRIES.txt
    ├── SQL-Data/
    │   ├── 01-FINTECH-REGIONS.sql
    │   ├── 02-FINTECH-COUNTRIES.sql
    │   ├── 03-FINTECH-PAYMENT-METHODS.sql
    │   └── SQL-Data.zip
    └── README.md (este archivo)
```

## Ejecución del Pipeline

Una vez organizados los datos, puedes ejecutar el pipeline de carga siguiendo las instrucciones del README principal en la carpeta `pipelines/insert-data/`.

## Notas Importantes

- Los archivos en la carpeta `Bulk-Load` son versiones optimizadas para carga masiva de los scripts SQL originales.
- Los archivos en `FK-Values` contienen valores de claves foráneas utilizados para la generación de datos.
- No modifiques la estructura de los archivos SQL, ya que esto podría causar errores durante la ejecución del pipeline.