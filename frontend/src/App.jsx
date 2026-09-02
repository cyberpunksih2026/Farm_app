import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { ThemeProvider } from './context/ThemeContext';
import { ToastProvider } from './context/ToastContext';
import { SyncProvider } from './context/SyncContext';

// Customer Components & Guards
import { CustomerProtectedRoute } from './components/customer/CustomerProtectedRoute';

// Customer Pages
import { CustomerHome } from './pages/customer/CustomerHome';
import { ProductDetail } from './pages/customer/ProductDetail';
import { CartPage } from './pages/customer/CartPage';
import { CustomerLogin } from './pages/customer/CustomerLogin';
import { CustomerRegister } from './pages/customer/CustomerRegister';
import { CheckoutPlaceholder } from './pages/customer/CheckoutPlaceholder';

// Auth Recovery Pages
import { ForgotPassword } from './pages/ForgotPassword';
import { ResetPassword } from './pages/ResetPassword';
import { VerifyEmail } from './pages/VerifyEmail';

// Internal Admin / Operations Layouts & Pages (Preserved)
import { MainLayout } from './components/layout/MainLayout';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import { Dashboard } from './pages/Dashboard';
import { AuditLogs } from './pages/AuditLogs';
import { Settings } from './pages/Settings';
import { UsersPage } from './pages/Users';
import { SyncConflicts } from './pages/SyncConflicts';
import { RegisteredDevices } from './pages/RegisteredDevices';
import { NotFound } from './pages/NotFound';

export const App = () => {
  return (
    <ThemeProvider>
      <ToastProvider>
        <AuthProvider>
          <CartProvider>
            <SyncProvider>
              <BrowserRouter>
                <Routes>
                  {/* Public Customer Marketplace Routes */}
                  <Route path="/" element={<CustomerHome />} />
                  <Route path="/product/:id" element={<ProductDetail />} />
                  <Route path="/products/:id" element={<ProductDetail />} />
                  <Route path="/cart" element={<CartPage />} />

                  {/* Customer Authentication */}
                  <Route path="/login" element={<CustomerLogin />} />
                  <Route path="/register" element={<CustomerRegister />} />
                  <Route path="/forgot-password" element={<ForgotPassword />} />
                  <Route path="/reset-password" element={<ResetPassword />} />
                  <Route path="/verify-email" element={<VerifyEmail />} />

                  {/* Protected Customer Checkout */}
                  <Route
                    path="/checkout"
                    element={
                      <CustomerProtectedRoute>
                        <CheckoutPlaceholder />
                      </CustomerProtectedRoute>
                    }
                  />

                  {/* Internal Admin / Operations Routes (Preserved) */}
                  <Route
                    path="/admin"
                    element={
                      <ProtectedRoute requireAdmin>
                        <MainLayout />
                      </ProtectedRoute>
                    }
                  >
                    <Route index element={<Dashboard />} />
                    <Route path="dashboard" element={<Dashboard />} />
                    <Route path="users" element={<UsersPage />} />
                    <Route path="audit-logs" element={<AuditLogs />} />
                    <Route path="settings" element={<Settings />} />
                    <Route path="devices" element={<RegisteredDevices />} />
                    <Route path="sync-conflicts" element={<SyncConflicts />} />
                  </Route>

                  {/* 404 Catch-all */}
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </BrowserRouter>
            </SyncProvider>
          </CartProvider>
        </AuthProvider>
      </ToastProvider>
    </ThemeProvider>
  );
};

export default App;
