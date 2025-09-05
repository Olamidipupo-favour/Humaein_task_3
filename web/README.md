# RCM GCC Web Frontend

Modern, responsive web application for AI-native Revenue Cycle Management in GCC healthcare.

## Features

- **Modern UI**: Built with Next.js 14, TypeScript, and TailwindCSS
- **AI Integration**: Real-time AI assistance for RCM workflows
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Interactive Charts**: Data visualization with Recharts
- **Smooth Animations**: Framer Motion for delightful interactions
- **Role-based Access**: Different interfaces for Admin, Biller, Coder, and Analyst roles

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: TailwindCSS with shadcn/ui components
- **State Management**: React hooks with SWR
- **Charts**: Recharts for data visualization
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Forms**: React Hook Form with Zod validation

## Quick Start

### Prerequisites

- Node.js 18+
- Yarn package manager
- API backend running (see API documentation)

### Development Setup

1. **Install dependencies:**
   ```bash
   yarn install
   ```

2. **Set up environment:**
   ```bash
   cp env.example .env.local
   # Edit .env.local with your configuration
   ```

3. **Start development server:**
   ```bash
   yarn dev
   ```

4. **Access the application:**
   - Open http://localhost:3001
   - Use demo credentials: admin@demo.com / admin123

### Production Build

```bash
# Build the application
yarn build

# Start production server
yarn start

# Run linting
yarn lint

# Type checking
yarn type-check
```

## Project Structure

```
web/
├── app/                    # Next.js App Router pages
│   ├── dashboard/         # Dashboard layout and pages
│   ├── (rcm)/            # RCM workflow pages
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Landing page
├── components/            # Reusable components
│   ├── ui/               # shadcn/ui components
│   ├── charts/           # Chart components
│   └── ai/               # AI assistant components
├── lib/                  # Utility functions
├── public/               # Static assets
└── docs/                 # Documentation
```

## Key Components

### Dashboard Layout
- Responsive sidebar navigation
- Role-based access control
- Mobile-friendly design
- Smooth transitions

### RCM Workflows
- **Eligibility**: Patient coverage verification
- **Prior Auth**: Authorization requirements
- **Medical Coding**: ICD-10/CPT suggestions
- **Claims Scrubbing**: Pre-submission validation
- **Claims Submission**: Electronic filing
- **Remittance**: Payment tracking
- **Denials**: Appeal management
- **Reconciliation**: Financial reconciliation

### AI Assistant
- Context-aware suggestions
- Real-time assistance
- Workflow-specific prompts
- Confidence scoring

## Styling and Design

### Design System
- **Colors**: Consistent color palette with CSS variables
- **Typography**: Inter font family
- **Spacing**: TailwindCSS spacing scale
- **Shadows**: Soft, modern shadow system
- **Border Radius**: Consistent rounded corners

### Responsive Design
- Mobile-first approach
- Breakpoint system: sm, md, lg, xl, 2xl
- Flexible layouts with CSS Grid and Flexbox
- Touch-friendly interactions

### Accessibility
- ARIA labels and roles
- Keyboard navigation
- Screen reader support
- High contrast mode support

## API Integration

### Data Fetching
- SWR for caching and revalidation
- Optimistic updates
- Error handling and retries
- Loading states

### Authentication
- Role-based demo system
- Local storage for session management
- Protected routes
- Automatic logout

## Performance Optimization

### Code Splitting
- Automatic route-based splitting
- Component-level lazy loading
- Dynamic imports for heavy components

### Image Optimization
- Next.js Image component
- Automatic format optimization
- Responsive images
- Lazy loading

### Caching
- SWR caching strategy
- Static generation where possible
- CDN-ready assets

## Development Guidelines

### Code Style
- TypeScript strict mode
- ESLint configuration
- Prettier formatting
- Husky pre-commit hooks

### Component Patterns
- Functional components with hooks
- Props interface definitions
- Error boundaries
- Loading states

### State Management
- React hooks for local state
- SWR for server state
- Context for global state
- Local storage for persistence

## Testing

### Unit Testing
```bash
# Run unit tests
yarn test

# Run with coverage
yarn test --coverage
```

### E2E Testing
```bash
# Run E2E tests
yarn test:e2e
```

## Deployment

### Docker Deployment
```bash
# Build Docker image
docker build -t rcm-gcc-web .

# Run container
docker run -p 3001:3001 rcm-gcc-web
```

### Environment Variables
- `NEXT_PUBLIC_API_BASE_URL`: API server URL
- `DEMO_LOGIN`: Enable demo login mode
- `NEXT_TELEMETRY_DISABLED`: Disable telemetry

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

- **Documentation**: See `/docs` folder
- **Issues**: GitHub Issues
- **Contact**: contact@humaein.com

## License

Built for Humaein - All rights reserved.

