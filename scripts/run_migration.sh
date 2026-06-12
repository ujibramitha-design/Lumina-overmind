#!/bin/bash

# LUMINA OS - Database Migration Script
# Run Prisma migrations for new ImportedSiteplan table

echo "🗄️ Running database migrations for Siteplan Dropzone..."

# Check if Prisma is installed
if ! command -v npx &> /dev/null; then
    echo "❌ npx not found. Please install Node.js and npm first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create .env file first."
    exit 1
fi

# Run Prisma migrations
echo "🔄 Generating Prisma client..."
npx prisma generate

echo "🔄 Running database migration..."
npx prisma migrate dev --name add_imported_siteplan

echo "🔄 Pushing schema to database..."
npx prisma db push

echo "✅ Migration completed successfully!"
echo ""
echo "📋 New table created: ImportedSiteplan"
echo "🔗 Ready for siteplan uploads and VFX processing"
echo ""
echo "🚀 You can now access the Siteplan Dropzone at:"
echo "   http://localhost:3000/dashboard/assets/siteplan-dropzone"
