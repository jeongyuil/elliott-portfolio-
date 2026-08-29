import { Component, type ErrorInfo, type ReactNode } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RefreshCcw, AlertTriangle } from "lucide-react";

interface Props {
    children: ReactNode;
    scope?: string; // e.g., "Global", "Adventure"
}

interface State {
    hasError: boolean;
    error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false,
        error: null,
    };

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error(`[ErrorBoundary:${this.props.scope || "root"}]`, error, errorInfo);
    }

    private handleRetry = () => {
        this.setState({ hasError: false, error: null });
        window.location.reload();
    };

    public render() {
        if (this.state.hasError) {
            return (
                <div className="flex items-center justify-center min-h-[50vh] p-6">
                    <Card className="max-w-md w-full shadow-lg border-destructive/20">
                        <CardHeader className="flex flex-col items-center text-center pb-2">
                            <div className="h-12 w-12 rounded-full bg-red-100 flex items-center justify-center mb-4 text-red-600">
                                <AlertTriangle className="h-6 w-6" />
                            </div>
                            <CardTitle className="text-xl text-destructive font-bold">
                                오류가 발생했습니다
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="text-center space-y-6">
                            <p className="text-muted-foreground text-sm">
                                죄송합니다. 일시적인 오류가 발생했습니다.<br />
                                잠시 후 다시 시도해주세요.
                            </p>

                            {/* Dev Only Error Details */}
                            {import.meta.env.DEV && this.state.error && (
                                <div className="text-xs text-left bg-muted p-3 rounded-md overflow-auto max-h-32 font-mono">
                                    {this.state.error.toString()}
                                </div>
                            )}

                            <Button onClick={this.handleRetry} className="w-full" variant="secondary">
                                <RefreshCcw className="mr-2 h-4 w-4" />
                                페이지 새로고침
                            </Button>
                        </CardContent>
                    </Card>
                </div>
            );
        }

        return this.props.children;
    }
}
