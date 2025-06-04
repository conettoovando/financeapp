type Props = {
  children: React.ReactNode;
};

export default function Container({ children }: Props) {
  return <div className="p-4 mx-auto h-[98vh]">{children}</div>;
}
