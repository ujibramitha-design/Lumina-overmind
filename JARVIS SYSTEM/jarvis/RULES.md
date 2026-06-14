# JARVIS Strict Development Rules

Aturan ketat untuk pengembangan JARVIS AI System.

## Struktur Folder

```
jarvis/
├── core/              # Core system files
├── channels/          # Communication channels
├── security/          # Security layer
├── intelligence/      # AI intelligence
├── omniscient/        # Document ingestion
├── economics/         # Economic modules
├── shadow_ceo/        # CEO modules
├── creative/          # Creative modules
├── finance/           # Financial modules
├── revenue/           # Revenue modules
├── business/          # Business modules
├── empire/            # Empire modules
├── invisible/         # Invisible modules
├── corporation/       # AI Corporation
├── hardware/          # Hardware bridge
├── hydra/             # Multi-cloud protocol
├── legacy/            # Legacy protocol
├── python/            # Python scripts
├── data/              # Data directory
├── logs/              # Log directory
├── docs/              # Documentation
└── mobile/            # Mobile app
```

## Aturan Pengembangan

### 1. Isolasi Kode
- **WAJIB**: JARVIS harus 100% terisolasi dari lumina-overmind
- **WAJIB**: Tidak ada import langsung dari lumina-overmind ke JARVIS
- **WAJIB**: Gunakan REST API/WebSocket untuk komunikasi antar sistem
- **WAJIB**: Setiap modul harus independent dan self-contained

### 2. Security
- **WAJIB**: Creator Security Layer harus selalu aktif
- **WAJIB**: Semua API keys harus di environment variables
- **WAJIB**: Jangan hardcode credentials di kode
- **WAJIB**: Gunakan encryption untuk sensitive data
- **WAJIB**: Log semua security events

### 3. Error Handling
- **WAJIB**: Semua async functions harus try-catch
- **WAJIB**: Log semua errors dengan detail
- **WAJIB**: Gunakan graceful degradation
- **WAJIB**: Implement retry logic untuk network calls
- **WAJIB**: Fallback mechanism untuk critical services

### 4. Git Workflow
- **WAJIB**: Gunakan feature branches untuk development
- **WAJIB**: Pull request harus di-review sebelum merge
- **WAJIB**: Commit messages harus descriptive
- **WAJIB**: Jangan commit sensitive data (.env, keys)
- **WAJIB**: Update .gitignore untuk semua sensitive files

### 5. Testing
- **WAJIB**: Unit tests untuk semua critical functions
- **WAJIB**: Integration tests untuk API endpoints
- **WAJIB**: Test security layer secara terpisah
- **WAJIB**: Test failover mechanisms
- **WAJIB**: Test emergency protocols

### 6. Documentation
- **WAJIB**: JSDoc comments untuk semua functions
- **WAJIB**: Update README.md untuk setiap major change
- **WAJIB**: Document semua environment variables
- **WAJIB**: Document API endpoints
- **WAJIB**: Document emergency procedures

### 7. Performance
- **WAJIB**: Monitor memory usage
- **WAJIB**: Implement caching untuk expensive operations
- **WAJIB**: Optimize database queries
- **WAJIB**: Use connection pooling
- **WAJIB**: Implement rate limiting

### 8. Monitoring
- **WAJIB**: Log semua critical operations
- **WAJIB**: Implement health check endpoints
- **WAJIB**: Monitor system resources
- **WAJIB**: Alert untuk critical failures
- **WAJIB**: Track uptime and availability

## Aturan Spesifik Modul

### Security Layer
- Creator ID harus di environment variables
- God Mode hanya untuk Creator
- Terminate Protocol hanya untuk Creator
- Log semua Creator access

### Intelligence Layer
- Gemini API harus punya fallback ke Ollama
- Timeout harus < 10 detik
- Implement retry logic
- Monitor provider health

### Financial Layer
- Double-entry bookkeeping harus validated
- Database transactions harus atomic
- Log semua financial operations
- Implement audit trail

### Hardware Layer
- MQTT harus authenticated
- Physical reboot harus double-confirmed
- Log semua hardware commands
- Implement safety protocols

### Legacy Protocol
- Dead Man's Switch harus tested regularly
- Emergency contacts harus up-to-date
- Asset liquidation harus multi-confirmed
- Log semua legacy protocol actions

## Environment Variables

```bash
# Core
NODE_ENV=production
JARVIS_PORT=3001
LUMINA_API_URL=http://localhost:8000

# Security
ROOT_CREATOR_WA_NUMBER=your_wa_number
ROOT_CREATOR_TG_ID=your_tg_id
ROOT_CREATOR_VERIFICATION_TOKEN=your_token

# AI
GEMINI_API_KEY=your_gemini_key
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3

# Financial
JARVIS_WALLET_PRIVATE_KEY=your_wallet_key
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
STRIPE_SECRET_KEY=your_stripe_key

# IoT
MQTT_BROKER=mqtt://localhost:1883
MQTT_USERNAME=jarvis
MQTT_PASSWORD=secure_password

# Cloudflare
CLOUDFLARE_API_TOKEN=your_cloudflare_token
CLOUDFLARE_ZONE_ID=your_zone_id

# Legacy
NEXT_OF_KIN_EMAIL=next_of_kin@example.com
NEXT_OF_KIN_PHONE=+1234567890
NEXT_OF_KIN_ADDRESS=0x1234567890abcdef1234567890abcdef12345678
```

## Git Workflow

### Branch Naming
- `feature/feature-name` untuk new features
- `bugfix/bug-description` untuk bug fixes
- `hotfix/critical-fix` untuk urgent fixes
- `refactor/refactor-description` untuk refactoring

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

### Example
```
feat(security): add creator middleware for god mode

- Implement creator ID verification
- Add god mode override command
- Add terminate protocol command
- Update gemini service with creator obedience

Closes #123
```

## Deployment

### Development
```bash
npm install
npm run dev
```

### Production
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Monitoring
```bash
pm2 logs jarvis-app
pm2 monit
pm2 status
```

## Emergency Procedures

### Creator Emergency Access
1. Gunakan Creator credentials
2. Aktifkan God Mode dengan `/override`
3. Execute emergency command
4. Monitor system response

### System Failure
1. Check PM2 status
2. Check logs
3. Restart affected services
4. Verify health endpoints

### Security Breach
1. Activate Directive Lock
2. Isolate affected systems
3. Review audit logs
4. Rotate all credentials
5. Notify Creator

## Code Quality

### JavaScript/TypeScript
- Gunakan ES6+ features
- Gunakan async/await untuk async operations
- Gunakan const/let, jangan var
- Gunakan arrow functions untuk callbacks
- Gunakan template literals untuk strings

### Python
- Gunakan type hints
- Gunakan docstrings untuk functions
- Gunakan f-strings untuk string formatting
- Gunakan context managers untuk resources
- Gunakan exception handling

### Database
- Gunakan prepared statements
- Gunakan transactions untuk multiple operations
- Implement connection pooling
- Index critical columns
- Regular backups

## Forbidden Actions

❌ **DILARANG**:
- Hardcode credentials
- Commit .env files
- Bypass security checks
- Ignore error handling
- Skip testing
- Commit broken code
- Merge without review
- Disable logging
- Ignore security warnings
- Skip documentation

## Approval Process

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Error handling implemented
- [ ] Security considerations addressed
- [ ] Tests included
- [ ] Documentation updated
- [ ] No sensitive data committed
- [ ] Performance considered
- [ ] Backward compatibility maintained

### Deployment Checklist
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Backup taken
- [ ] Rollback plan ready
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Team notified

## Contact

Untuk pertanyaan atau issues:
- Review documentation
- Check logs
- Contact Creator for critical issues
- Use proper channels for non-critical issues

## Version History

- v1.0.0 - Initial JARVIS system
- v2.0.0 - Added Creator Security Layer
- v3.0.0 - Added Elite Modules
- v4.0.0 - Added Fault Tolerance
- v5.0.0 - Added Absolute Resilience
- v6.0.0 - Added Decentralized Entity

## License

JARVIS AI System - Proprietary
All rights reserved
